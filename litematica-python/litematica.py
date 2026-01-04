"""
Litematica schematic file format reader and writer.

This module provides classes for reading, writing, and manipulating Litematica
schematic files (.litematic) used in Minecraft.
"""

import gzip
import struct
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from nbt import nbt


class BlockState:
    """Represents a Minecraft block state with properties."""
    
    def __init__(self, name: str, properties: Optional[Dict[str, str]] = None):
        """
        Initialize a block state.
        
        Args:
            name: Block ID (e.g., "minecraft:stone")
            properties: Block properties (e.g., {"facing": "north"})
        """
        self.name = name
        self.properties = properties or {}
    
    def __eq__(self, other):
        if not isinstance(other, BlockState):
            return False
        return self.name == other.name and self.properties == other.properties
    
    def __hash__(self):
        return hash((self.name, tuple(sorted(self.properties.items()))))
    
    def __repr__(self):
        if self.properties:
            props = ", ".join(f"{k}={v}" for k, v in sorted(self.properties.items()))
            return f"BlockState({self.name}[{props}])"
        return f"BlockState({self.name})"
    
    def to_nbt(self) -> nbt.TAG_Compound:
        """Convert block state to NBT format."""
        tag = nbt.TAG_Compound()
        tag.tags.append(nbt.TAG_String(name="Name", value=self.name))
        
        if self.properties:
            props_tag = nbt.TAG_Compound()
            props_tag.name = "Properties"
            for key, value in self.properties.items():
                props_tag.tags.append(nbt.TAG_String(name=key, value=value))
            tag.tags.append(props_tag)
        
        return tag
    
    @staticmethod
    def from_nbt(tag: nbt.TAG_Compound) -> 'BlockState':
        """Create block state from NBT format."""
        name = tag["Name"].value
        properties = {}
        
        if "Properties" in tag:
            props_tag = tag["Properties"]
            for prop in props_tag.tags:
                properties[prop.name] = prop.value
        
        return BlockState(name, properties)


class BitArray:
    """Packed long array for efficient block state storage."""
    
    def __init__(self, bits_per_entry: int, size: int, data: Optional[List[int]] = None):
        """
        Initialize a bit array.
        
        Args:
            bits_per_entry: Number of bits per value (2-32)
            size: Number of entries to store
            data: Optional pre-existing long array data
        """
        if not 1 <= bits_per_entry <= 32:
            raise ValueError("bits_per_entry must be between 1 and 32")
        
        self.bits_per_entry = bits_per_entry
        self.size = size
        self.max_value = (1 << bits_per_entry) - 1
        
        # Calculate required number of longs
        total_bits = size * bits_per_entry
        long_count = (total_bits + 63) // 64  # Round up
        
        if data is not None:
            self.data = list(data)
        else:
            self.data = [0] * long_count
    
    def get(self, index: int) -> int:
        """Get value at index."""
        if not 0 <= index < self.size:
            raise IndexError(f"Index {index} out of range [0, {self.size})")
        
        start_bit = index * self.bits_per_entry
        start_long = start_bit // 64
        end_long = ((index + 1) * self.bits_per_entry - 1) // 64
        start_bit_offset = start_bit % 64
        
        if start_long == end_long:
            # Value is within a single long
            return (self.data[start_long] >> start_bit_offset) & self.max_value
        else:
            # Value spans two longs
            end_offset = 64 - start_bit_offset
            part1 = self.data[start_long] >> start_bit_offset
            part2 = self.data[end_long] << end_offset
            return (part1 | part2) & self.max_value
    
    def set(self, index: int, value: int):
        """Set value at index."""
        if not 0 <= index < self.size:
            raise IndexError(f"Index {index} out of range [0, {self.size})")
        if not 0 <= value <= self.max_value:
            raise ValueError(f"Value {value} out of range [0, {self.max_value}]")
        
        start_bit = index * self.bits_per_entry
        start_long = start_bit // 64
        end_long = ((index + 1) * self.bits_per_entry - 1) // 64
        start_bit_offset = start_bit % 64
        
        # Clear the bits for this entry
        mask = self.max_value << start_bit_offset
        self.data[start_long] = (self.data[start_long] & ~mask) | ((value & self.max_value) << start_bit_offset)
        
        if start_long != end_long:
            # Value spans two longs
            end_offset = 64 - start_bit_offset
            remaining_bits = self.bits_per_entry - end_offset
            mask = (1 << remaining_bits) - 1
            self.data[end_long] = (self.data[end_long] >> remaining_bits << remaining_bits) | ((value & self.max_value) >> end_offset)


class Region:
    """Represents a region within a Litematica schematic."""
    
    def __init__(self, name: str, position: Tuple[int, int, int], size: Tuple[int, int, int]):
        """
        Initialize a region.
        
        Args:
            name: Region name
            position: (x, y, z) position relative to schematic origin
            size: (x, y, z) dimensions
        """
        self.name = name
        self.position = position
        self.size = size
        self.palette: List[BlockState] = [BlockState("minecraft:air")]
        self.palette_map: Dict[BlockState, int] = {self.palette[0]: 0}
        self.volume = size[0] * size[1] * size[2]
        
        # Initialize with air (palette ID 0)
        bits_per_entry = max(2, (len(self.palette) - 1).bit_length())
        self.block_states = BitArray(bits_per_entry, self.volume)
        
        self.block_entities: Dict[Tuple[int, int, int], nbt.TAG_Compound] = {}
        self.entities: List[nbt.TAG_Compound] = []
        self.pending_ticks: List[nbt.TAG_Compound] = []
    
    def _get_index(self, x: int, y: int, z: int) -> int:
        """Convert (x, y, z) to linear index (YZX order)."""
        if not (0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.size[2]):
            raise ValueError(f"Position ({x}, {y}, {z}) out of bounds for size {self.size}")
        return y * (self.size[0] * self.size[2]) + z * self.size[0] + x
    
    def _add_to_palette(self, state: BlockState) -> int:
        """Add block state to palette if not present, return its ID."""
        if state in self.palette_map:
            return self.palette_map[state]
        
        palette_id = len(self.palette)
        self.palette.append(state)
        self.palette_map[state] = palette_id
        
        # Check if we need to resize the bit array
        new_bits = max(2, (len(self.palette) - 1).bit_length())
        if new_bits > self.block_states.bits_per_entry:
            self._resize_bit_array(new_bits)
        
        return palette_id
    
    def _resize_bit_array(self, new_bits: int):
        """Resize bit array when palette grows."""
        old_array = self.block_states
        self.block_states = BitArray(new_bits, self.volume)
        
        # Copy all values
        for i in range(self.volume):
            self.block_states.set(i, old_array.get(i))
    
    def get_block(self, x: int, y: int, z: int) -> BlockState:
        """Get block state at position."""
        index = self._get_index(x, y, z)
        palette_id = self.block_states.get(index)
        return self.palette[palette_id]
    
    def set_block(self, x: int, y: int, z: int, state: BlockState):
        """Set block state at position."""
        palette_id = self._add_to_palette(state)
        index = self._get_index(x, y, z)
        self.block_states.set(index, palette_id)
    
    def set_block_entity(self, x: int, y: int, z: int, entity_data: nbt.TAG_Compound):
        """Set block entity data at position."""
        self.block_entities[(x, y, z)] = entity_data
    
    def get_block_entity(self, x: int, y: int, z: int) -> Optional[nbt.TAG_Compound]:
        """Get block entity data at position."""
        return self.block_entities.get((x, y, z))


class SchematicMetadata:
    """Metadata for a Litematica schematic."""
    
    def __init__(self):
        self.name = "?"
        self.author = "?"
        self.description = ""
        self.region_count = 0
        self.total_volume = 0
        self.total_blocks = 0
        self.time_created = int(datetime.now().timestamp() * 1000)
        self.time_modified = self.time_created
        self.enclosing_size = (0, 0, 0)
        self.preview_image_data: Optional[List[int]] = None
    
    def to_nbt(self) -> nbt.TAG_Compound:
        """Convert metadata to NBT format."""
        tag = nbt.TAG_Compound()
        tag.tags.append(nbt.TAG_String(name="Name", value=self.name))
        tag.tags.append(nbt.TAG_String(name="Author", value=self.author))
        tag.tags.append(nbt.TAG_String(name="Description", value=self.description))
        
        if self.region_count > 0:
            tag.tags.append(nbt.TAG_Int(name="RegionCount", value=self.region_count))
        if self.total_volume > 0:
            tag.tags.append(nbt.TAG_Long(name="TotalVolume", value=self.total_volume))
        if self.total_blocks >= 0:
            tag.tags.append(nbt.TAG_Long(name="TotalBlocks", value=self.total_blocks))
        if self.time_created > 0:
            tag.tags.append(nbt.TAG_Long(name="TimeCreated", value=self.time_created))
        if self.time_modified > 0:
            tag.tags.append(nbt.TAG_Long(name="TimeModified", value=self.time_modified))
        
        # Enclosing size
        size_tag = nbt.TAG_Compound()
        size_tag.name = "EnclosingSize"
        size_tag.tags.append(nbt.TAG_Int(name="x", value=self.enclosing_size[0]))
        size_tag.tags.append(nbt.TAG_Int(name="y", value=self.enclosing_size[1]))
        size_tag.tags.append(nbt.TAG_Int(name="z", value=self.enclosing_size[2]))
        tag.tags.append(size_tag)
        
        if self.preview_image_data:
            preview_tag = nbt.TAG_Int_Array(name="PreviewImageData")
            preview_tag.value = self.preview_image_data
            tag.tags.append(preview_tag)
        
        return tag
    
    @staticmethod
    def from_nbt(tag: nbt.TAG_Compound) -> 'SchematicMetadata':
        """Create metadata from NBT format."""
        metadata = SchematicMetadata()
        
        if "Name" in tag:
            metadata.name = tag["Name"].value
        if "Author" in tag:
            metadata.author = tag["Author"].value
        if "Description" in tag:
            metadata.description = tag["Description"].value
        if "RegionCount" in tag:
            metadata.region_count = tag["RegionCount"].value
        if "TotalVolume" in tag:
            metadata.total_volume = tag["TotalVolume"].value
        if "TotalBlocks" in tag:
            metadata.total_blocks = tag["TotalBlocks"].value
        if "TimeCreated" in tag:
            metadata.time_created = tag["TimeCreated"].value
        if "TimeModified" in tag:
            metadata.time_modified = tag["TimeModified"].value
        
        if "EnclosingSize" in tag:
            size_tag = tag["EnclosingSize"]
            metadata.enclosing_size = (
                size_tag["x"].value,
                size_tag["y"].value,
                size_tag["z"].value
            )
        
        if "PreviewImageData" in tag:
            metadata.preview_image_data = list(tag["PreviewImageData"].value)
        
        return metadata


class LitematicaSchematic:
    """Litematica schematic file (.litematic)."""
    
    SCHEMATIC_VERSION = 4
    MINECRAFT_DATA_VERSION = 3465  # Minecraft 1.20.1
    FILE_EXTENSION = ".litematic"
    
    def __init__(self):
        self.metadata = SchematicMetadata()
        self.regions: Dict[str, Region] = {}
    
    def add_region(self, region: Region):
        """Add a region to the schematic."""
        self.regions[region.name] = region
    
    def get_region(self, name: str) -> Optional[Region]:
        """Get region by name."""
        return self.regions.get(name)
    
    def to_nbt(self) -> nbt.NBTFile:
        """Convert schematic to NBT format."""
        root = nbt.NBTFile()
        root.name = ""
        
        # Version and data version
        root.tags.append(nbt.TAG_Int(name="Version", value=self.SCHEMATIC_VERSION))
        root.tags.append(nbt.TAG_Int(name="MinecraftDataVersion", value=self.MINECRAFT_DATA_VERSION))
        
        # Metadata
        self.metadata.region_count = len(self.regions)
        metadata_tag = self.metadata.to_nbt()
        metadata_tag.name = "Metadata"
        root.tags.append(metadata_tag)
        
        # Regions
        regions_tag = nbt.TAG_Compound()
        regions_tag.name = "Regions"
        
        for region_name, region in self.regions.items():
            region_tag = nbt.TAG_Compound()
            region_tag.name = region_name
            
            # Position
            pos_tag = nbt.TAG_Compound()
            pos_tag.name = "Position"
            pos_tag.tags.append(nbt.TAG_Int(name="x", value=region.position[0]))
            pos_tag.tags.append(nbt.TAG_Int(name="y", value=region.position[1]))
            pos_tag.tags.append(nbt.TAG_Int(name="z", value=region.position[2]))
            region_tag.tags.append(pos_tag)
            
            # Size
            size_tag = nbt.TAG_Compound()
            size_tag.name = "Size"
            size_tag.tags.append(nbt.TAG_Int(name="x", value=region.size[0]))
            size_tag.tags.append(nbt.TAG_Int(name="y", value=region.size[1]))
            size_tag.tags.append(nbt.TAG_Int(name="z", value=region.size[2]))
            region_tag.tags.append(size_tag)
            
            # Block state palette
            palette_list = nbt.TAG_List(name="BlockStatePalette", type=nbt.TAG_Compound)
            for block_state in region.palette:
                state_tag = block_state.to_nbt()
                palette_list.tags.append(state_tag)
            region_tag.tags.append(palette_list)
            
            # Block states (packed long array)
            import array
            # Convert unsigned 64-bit values to signed (Java uses signed longs)
            signed_data = []
            for val in region.block_states.data:
                # If value is > max signed long, convert to signed
                signed_val = val if val < (1 << 63) else val - (1 << 64)
                signed_data.append(signed_val)
            
            block_states_tag = nbt.TAG_Long_Array(name="BlockStates")
            block_states_tag.value = array.array('q', signed_data)
            region_tag.tags.append(block_states_tag)
            
            # Block entities
            if region.block_entities:
                be_list = nbt.TAG_List(name="TileEntities", type=nbt.TAG_Compound)
                for (x, y, z), be_data in region.block_entities.items():
                    be_tag = nbt.TAG_Compound()
                    be_tag.tags.extend(be_data.tags)
                    be_tag.tags.append(nbt.TAG_Int(name="x", value=x))
                    be_tag.tags.append(nbt.TAG_Int(name="y", value=y))
                    be_tag.tags.append(nbt.TAG_Int(name="z", value=z))
                    be_list.tags.append(be_tag)
                region_tag.tags.append(be_list)
            
            # Entities
            if region.entities:
                entity_list = nbt.TAG_List(name="Entities", type=nbt.TAG_Compound)
                for entity in region.entities:
                    entity_list.tags.append(entity)
                region_tag.tags.append(entity_list)
            
            # Pending ticks
            if region.pending_ticks:
                tick_list = nbt.TAG_List(name="PendingBlockTicks", type=nbt.TAG_Compound)
                for tick in region.pending_ticks:
                    tick_list.tags.append(tick)
                region_tag.tags.append(tick_list)
            
            regions_tag.tags.append(region_tag)
        
        root.tags.append(regions_tag)
        return root
    
    @staticmethod
    def from_nbt(nbt_file: nbt.NBTFile) -> 'LitematicaSchematic':
        """Create schematic from NBT format."""
        schematic = LitematicaSchematic()
        
        # Check version
        if "Version" not in nbt_file:
            raise ValueError("Missing Version tag")
        
        version = nbt_file["Version"].value
        if version < 1 or version > LitematicaSchematic.SCHEMATIC_VERSION:
            raise ValueError(f"Unsupported schematic version: {version}")
        
        # Read metadata
        if "Metadata" in nbt_file:
            schematic.metadata = SchematicMetadata.from_nbt(nbt_file["Metadata"])
        
        # Read regions
        if "Regions" not in nbt_file:
            raise ValueError("Missing Regions tag")
        
        regions_tag = nbt_file["Regions"]
        for region_tag in regions_tag.tags:
            region_name = region_tag.name
            
            # Position
            pos_tag = region_tag["Position"]
            position = (pos_tag["x"].value, pos_tag["y"].value, pos_tag["z"].value)
            
            # Size
            size_tag = region_tag["Size"]
            size = (size_tag["x"].value, size_tag["y"].value, size_tag["z"].value)
            
            region = Region(region_name, position, size)
            
            # Palette
            palette_list = region_tag["BlockStatePalette"]
            region.palette = [BlockState.from_nbt(tag) for tag in palette_list.tags]
            region.palette_map = {state: i for i, state in enumerate(region.palette)}
            
            # Block states
            block_states_data = list(region_tag["BlockStates"].value)
            bits_per_entry = max(2, (len(region.palette) - 1).bit_length())
            region.block_states = BitArray(bits_per_entry, region.volume, block_states_data)
            
            # Block entities
            if "TileEntities" in region_tag:
                for be_tag in region_tag["TileEntities"].tags:
                    x = be_tag["x"].value
                    y = be_tag["y"].value
                    z = be_tag["z"].value
                    
                    # Create copy without position tags
                    be_data = nbt.TAG_Compound()
                    for tag in be_tag.tags:
                        if tag.name not in ("x", "y", "z"):
                            be_data.tags.append(tag)
                    
                    region.block_entities[(x, y, z)] = be_data
            
            # Entities
            if "Entities" in region_tag:
                region.entities = list(region_tag["Entities"].tags)
            
            # Pending ticks
            if "PendingBlockTicks" in region_tag:
                region.pending_ticks = list(region_tag["PendingBlockTicks"].tags)
            
            schematic.regions[region_name] = region
        
        return schematic
    
    def save(self, filename: str):
        """Save schematic to file."""
        if not filename.endswith(self.FILE_EXTENSION):
            filename += self.FILE_EXTENSION
        
        nbt_data = self.to_nbt()
        nbt_data.write_file(filename)
    
    @staticmethod
    def load(filename: str) -> 'LitematicaSchematic':
        """Load schematic from file."""
        nbt_data = nbt.NBTFile(filename, 'rb')
        return LitematicaSchematic.from_nbt(nbt_data)
    
    def __repr__(self):
        return f"LitematicaSchematic(name='{self.metadata.name}', regions={len(self.regions)})"


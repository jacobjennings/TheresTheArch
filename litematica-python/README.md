# Litematica Python Library

A Python library for reading, writing, and manipulating Litematica schematic files (.litematic) used in Minecraft.

## Features

- ✅ Read and write Litematica schematic files (version 1-4)
- ✅ Support for multiple regions per schematic
- ✅ Full block state support with properties
- ✅ Block entities (chests, signs, etc.)
- ✅ Entity support (mobs, item frames, etc.)
- ✅ Pending block ticks
- ✅ Schematic metadata (name, author, description, timestamps)
- ✅ Efficient bit-packed block storage
- ✅ Preview image support

## Installation

### From Source

```bash
cd litematica-python
pip install -r requirements.txt
```

### Dependencies

- Python 3.7+
- NBT library for Python

```bash
pip install NBT
```

## Quick Start

### Loading a Schematic

```python
from litematica import LitematicaSchematic

# Load schematic from file
schematic = LitematicaSchematic.load("my_build.litematic")

# Access metadata
print(f"Name: {schematic.metadata.name}")
print(f"Author: {schematic.metadata.author}")
print(f"Regions: {len(schematic.regions)}")

# Access regions
for region_name, region in schematic.regions.items():
    print(f"Region '{region_name}': {region.size}")
```

### Creating a New Schematic

```python
from litematica import LitematicaSchematic, Region, BlockState

# Create schematic
schematic = LitematicaSchematic()
schematic.metadata.name = "My Build"
schematic.metadata.author = "Player123"
schematic.metadata.description = "A cool structure"

# Create region
region = Region("Main", position=(0, 0, 0), size=(10, 10, 10))

# Set blocks
stone = BlockState("minecraft:stone")
region.set_block(0, 0, 0, stone)

# Add stairs with properties
stairs = BlockState("minecraft:oak_stairs", {
    "facing": "north",
    "half": "bottom",
    "shape": "straight"
})
region.set_block(1, 0, 0, stairs)

# Add region to schematic
schematic.add_region(region)

# Save
schematic.save("my_build.litematic")
```

### Working with Blocks

```python
# Get block at position
block = region.get_block(5, 10, 3)
print(f"Block: {block.name}")
print(f"Properties: {block.properties}")

# Set multiple blocks
grass = BlockState("minecraft:grass_block")
for x in range(10):
    for z in range(10):
        region.set_block(x, 0, z, grass)
```

### Working with Block Entities

```python
from nbt import nbt

# Create a chest with items
chest_data = nbt.TAG_Compound()
chest_data.tags.append(nbt.TAG_String(name="id", value="minecraft:chest"))

# Add items
items_list = nbt.TAG_List(name="Items", type=nbt.TAG_Compound)
item = nbt.TAG_Compound()
item.tags.append(nbt.TAG_String(name="id", value="minecraft:diamond"))
item.tags.append(nbt.TAG_Byte(name="Count", value=64))
item.tags.append(nbt.TAG_Byte(name="Slot", value=0))
items_list.tags.append(item)
chest_data.tags.append(items_list)

# Set block and block entity
chest_block = BlockState("minecraft:chest", {"facing": "north"})
region.set_block(5, 5, 5, chest_block)
region.set_block_entity(5, 5, 5, chest_data)
```

### Working with Entities

```python
# Create an armor stand entity
armor_stand = nbt.TAG_Compound()
armor_stand.tags.append(nbt.TAG_String(name="id", value="minecraft:armor_stand"))

# Position
pos_list = nbt.TAG_List(name="Pos", type=nbt.TAG_Double)
pos_list.tags.append(nbt.TAG_Double(value=5.5))
pos_list.tags.append(nbt.TAG_Double(value=64.0))
pos_list.tags.append(nbt.TAG_Double(value=3.5))
armor_stand.tags.append(pos_list)

# Properties
armor_stand.tags.append(nbt.TAG_Byte(name="NoGravity", value=1))
armor_stand.tags.append(nbt.TAG_Byte(name="ShowArms", value=1))

region.entities.append(armor_stand)
```

## API Reference

### LitematicaSchematic

Main schematic class.

**Methods:**
- `load(filename: str) -> LitematicaSchematic`: Load schematic from file
- `save(filename: str)`: Save schematic to file
- `add_region(region: Region)`: Add a region
- `get_region(name: str) -> Region`: Get region by name

**Attributes:**
- `metadata: SchematicMetadata`: Schematic metadata
- `regions: Dict[str, Region]`: Dictionary of regions

### SchematicMetadata

Schematic metadata.

**Attributes:**
- `name: str`: Schematic name
- `author: str`: Creator name
- `description: str`: Description
- `region_count: int`: Number of regions
- `total_volume: int`: Total volume in blocks
- `total_blocks: int`: Number of non-air blocks
- `time_created: int`: Creation timestamp (milliseconds)
- `time_modified: int`: Modification timestamp (milliseconds)
- `enclosing_size: Tuple[int, int, int]`: Overall dimensions
- `preview_image_data: List[int]`: Preview image pixels (ARGB)

### Region

A region within a schematic.

**Methods:**
- `get_block(x: int, y: int, z: int) -> BlockState`: Get block at position
- `set_block(x: int, y: int, z: int, state: BlockState)`: Set block at position
- `get_block_entity(x: int, y: int, z: int) -> TAG_Compound`: Get block entity
- `set_block_entity(x: int, y: int, z: int, data: TAG_Compound)`: Set block entity

**Attributes:**
- `name: str`: Region name
- `position: Tuple[int, int, int]`: Position relative to schematic origin
- `size: Tuple[int, int, int]`: Dimensions
- `palette: List[BlockState]`: Block state palette
- `block_entities: Dict[Tuple[int, int, int], TAG_Compound]`: Block entities
- `entities: List[TAG_Compound]`: Entities
- `pending_ticks: List[TAG_Compound]`: Pending block ticks

### BlockState

Represents a Minecraft block state.

**Constructor:**
```python
BlockState(name: str, properties: Dict[str, str] = None)
```

**Attributes:**
- `name: str`: Block ID (e.g., "minecraft:stone")
- `properties: Dict[str, str]`: Block properties

### BitArray

Packed long array for efficient storage (internal use).

**Methods:**
- `get(index: int) -> int`: Get value at index
- `set(index: int, value: int)`: Set value at index

## Examples

See [EXAMPLES.md](EXAMPLES.md) for more detailed examples including:
- Creating complex structures
- Working with multi-region schematics
- Converting between formats
- Manipulating existing schematics
- Performance optimization tips

## Format Documentation

See [FORMAT.md](FORMAT.md) for detailed documentation of the Litematica file format including:
- Complete NBT structure
- Block state palette format
- Bit packing algorithm
- Version history
- Compatibility notes

## Block State Examples

### Common Blocks

```python
# Simple blocks
air = BlockState("minecraft:air")
stone = BlockState("minecraft:stone")
dirt = BlockState("minecraft:dirt")
grass = BlockState("minecraft:grass_block")

# Logs with orientation
log = BlockState("minecraft:oak_log", {"axis": "y"})

# Stairs
stairs = BlockState("minecraft:oak_stairs", {
    "facing": "north",
    "half": "bottom",
    "shape": "straight",
    "waterlogged": "false"
})

# Slabs
slab = BlockState("minecraft:stone_slab", {
    "type": "bottom",
    "waterlogged": "false"
})

# Doors
door = BlockState("minecraft:oak_door", {
    "facing": "north",
    "half": "lower",
    "hinge": "left",
    "open": "false",
    "powered": "false"
})

# Redstone
redstone_wire = BlockState("minecraft:redstone_wire", {
    "east": "none",
    "north": "none",
    "power": "0",
    "south": "none",
    "west": "none"
})
```

## Performance Tips

1. **Batch Operations**: Set multiple blocks before accessing them to minimize palette resizing
2. **Pre-allocate Regions**: Create regions with correct size from the start
3. **Reuse BlockState Objects**: Create block states once and reuse them
4. **Minimize Palette Size**: Use fewer unique block states for better compression
5. **Large Schematics**: Consider using multiple regions to organize large builds

## Limitations

- Maximum palette size per region: 2^32 unique block states (theoretical)
- Practical palette size: ~2^16 for reasonable performance
- File size: Limited by available memory and disk space
- Block coordinates: Limited by NBT integer range (±2^31-1)

## Compatibility

- **Litematica Mod**: Fully compatible with Litematica for Minecraft 1.12.2 - 1.20+
- **Python Versions**: Requires Python 3.7 or higher
- **NBT Library**: Compatible with standard Python NBT library

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

See LICENSE file for details.

## Credits

Based on the Litematica mod by maruohon:
- https://github.com/maruohon/litematica

## See Also

- [FORMAT.md](FORMAT.md) - Complete file format specification
- [EXAMPLES.md](EXAMPLES.md) - Detailed usage examples
- [Litematica Mod](https://github.com/maruohon/litematica)
- [NBT Format](https://minecraft.fandom.com/wiki/NBT_format)


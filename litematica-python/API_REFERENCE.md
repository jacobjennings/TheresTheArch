# API Reference

Complete API documentation for the Litematica Python library.

## Table of Contents

- [LitematicaSchematic](#litematicaschematic)
- [Region](#region)
- [BlockState](#blockstate)
- [SchematicMetadata](#schematicmetadata)
- [BitArray](#bitarray)

---

## LitematicaSchematic

Main class for working with Litematica schematic files.

### Class Attributes

```python
SCHEMATIC_VERSION: int = 4
MINECRAFT_DATA_VERSION: int = 3465  # Minecraft 1.20.1
FILE_EXTENSION: str = ".litematic"
```

### Constructor

```python
LitematicaSchematic()
```

Creates a new empty schematic.

**Example:**
```python
schematic = LitematicaSchematic()
```

### Instance Attributes

#### `metadata: SchematicMetadata`
Schematic metadata (name, author, description, etc.).

#### `regions: Dict[str, Region]`
Dictionary of regions by name.

### Methods

#### `add_region(region: Region) -> None`
Add a region to the schematic.

**Parameters:**
- `region`: Region to add

**Example:**
```python
region = Region("Main", (0, 0, 0), (10, 10, 10))
schematic.add_region(region)
```

#### `get_region(name: str) -> Optional[Region]`
Get region by name.

**Parameters:**
- `name`: Region name

**Returns:**
- Region object if found, None otherwise

**Example:**
```python
region = schematic.get_region("Main")
if region:
    print(f"Found region with size {region.size}")
```

#### `save(filename: str) -> None`
Save schematic to file.

**Parameters:**
- `filename`: Output filename (`.litematic` extension added if not present)

**Raises:**
- `IOError`: If file cannot be written

**Example:**
```python
schematic.save("my_build.litematic")
```

#### `load(filename: str) -> LitematicaSchematic` (static)
Load schematic from file.

**Parameters:**
- `filename`: Input filename

**Returns:**
- LitematicaSchematic object

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If file format is invalid

**Example:**
```python
schematic = LitematicaSchematic.load("build.litematic")
```

#### `to_nbt() -> nbt.NBTFile`
Convert schematic to NBT format.

**Returns:**
- NBTFile object

**Example:**
```python
nbt_data = schematic.to_nbt()
```

#### `from_nbt(nbt_file: nbt.NBTFile) -> LitematicaSchematic` (static)
Create schematic from NBT format.

**Parameters:**
- `nbt_file`: NBT file object

**Returns:**
- LitematicaSchematic object

**Raises:**
- `ValueError`: If NBT structure is invalid

**Example:**
```python
nbt_data = nbt.NBTFile("build.litematic", 'rb')
schematic = LitematicaSchematic.from_nbt(nbt_data)
```

---

## Region

Represents a region within a schematic.

### Constructor

```python
Region(name: str, position: Tuple[int, int, int], size: Tuple[int, int, int])
```

**Parameters:**
- `name`: Region name
- `position`: (x, y, z) position relative to schematic origin
- `size`: (x, y, z) dimensions

**Example:**
```python
region = Region("Tower", position=(10, 0, 5), size=(10, 20, 10))
```

### Instance Attributes

#### `name: str`
Region name.

#### `position: Tuple[int, int, int]`
Position (x, y, z) relative to schematic origin.

#### `size: Tuple[int, int, int]`
Dimensions (width, height, depth).

#### `volume: int`
Total number of blocks (size.x × size.y × size.z).

#### `palette: List[BlockState]`
List of unique block states. Index 0 is always air.

#### `palette_map: Dict[BlockState, int]`
Maps block states to palette indices.

#### `block_entities: Dict[Tuple[int, int, int], nbt.TAG_Compound]`
Block entity data by position.

#### `entities: List[nbt.TAG_Compound]`
List of entities in the region.

#### `pending_ticks: List[nbt.TAG_Compound]`
List of scheduled block ticks.

### Methods

#### `get_block(x: int, y: int, z: int) -> BlockState`
Get block state at position.

**Parameters:**
- `x, y, z`: Position within region (0-indexed)

**Returns:**
- BlockState at that position

**Raises:**
- `ValueError`: If position is out of bounds

**Example:**
```python
block = region.get_block(5, 10, 3)
print(f"Block: {block.name}")
```

#### `set_block(x: int, y: int, z: int, state: BlockState) -> None`
Set block state at position.

**Parameters:**
- `x, y, z`: Position within region (0-indexed)
- `state`: BlockState to set

**Raises:**
- `ValueError`: If position is out of bounds

**Example:**
```python
stone = BlockState("minecraft:stone")
region.set_block(5, 10, 3, stone)
```

#### `get_block_entity(x: int, y: int, z: int) -> Optional[nbt.TAG_Compound]`
Get block entity data at position.

**Parameters:**
- `x, y, z`: Position within region

**Returns:**
- NBT compound with block entity data, or None if no block entity exists

**Example:**
```python
chest_data = region.get_block_entity(5, 5, 5)
if chest_data:
    print("Found a block entity")
```

#### `set_block_entity(x: int, y: int, z: int, entity_data: nbt.TAG_Compound) -> None`
Set block entity data at position.

**Parameters:**
- `x, y, z`: Position within region
- `entity_data`: NBT compound with block entity data

**Example:**
```python
chest_data = nbt.TAG_Compound()
chest_data.tags.append(nbt.TAG_String(name="id", value="minecraft:chest"))
region.set_block_entity(5, 5, 5, chest_data)
```

---

## BlockState

Represents a Minecraft block state with optional properties.

### Constructor

```python
BlockState(name: str, properties: Optional[Dict[str, str]] = None)
```

**Parameters:**
- `name`: Block ID (e.g., "minecraft:stone")
- `properties`: Optional dictionary of block properties

**Example:**
```python
# Simple block
stone = BlockState("minecraft:stone")

# Block with properties
stairs = BlockState("minecraft:oak_stairs", {
    "facing": "north",
    "half": "bottom",
    "shape": "straight"
})
```

### Instance Attributes

#### `name: str`
Block ID (e.g., "minecraft:stone").

#### `properties: Dict[str, str]`
Block properties dictionary.

### Methods

#### `to_nbt() -> nbt.TAG_Compound`
Convert block state to NBT format.

**Returns:**
- NBT compound representing the block state

**Example:**
```python
nbt_data = block_state.to_nbt()
```

#### `from_nbt(tag: nbt.TAG_Compound) -> BlockState` (static)
Create block state from NBT format.

**Parameters:**
- `tag`: NBT compound

**Returns:**
- BlockState object

**Example:**
```python
block_state = BlockState.from_nbt(nbt_tag)
```

### Special Methods

#### `__eq__(other) -> bool`
Check equality with another BlockState.

#### `__hash__() -> int`
Hash based on name and properties (for use in dictionaries/sets).

#### `__repr__() -> str`
String representation of the block state.

---

## SchematicMetadata

Metadata for a schematic.

### Constructor

```python
SchematicMetadata()
```

Creates metadata with default values.

### Instance Attributes

#### `name: str`
Schematic name (default: "?").

#### `author: str`
Creator name (default: "?").

#### `description: str`
Description text (default: "").

#### `region_count: int`
Number of regions (default: 0).

#### `total_volume: int`
Total volume in blocks (default: 0).

#### `total_blocks: int`
Number of non-air blocks (default: 0).

#### `time_created: int`
Creation timestamp in milliseconds.

#### `time_modified: int`
Last modification timestamp in milliseconds.

#### `enclosing_size: Tuple[int, int, int]`
Overall dimensions (default: (0, 0, 0)).

#### `preview_image_data: Optional[List[int]]`
Preview image pixels in ARGB format (default: None).

### Methods

#### `to_nbt() -> nbt.TAG_Compound`
Convert metadata to NBT format.

**Returns:**
- NBT compound

#### `from_nbt(tag: nbt.TAG_Compound) -> SchematicMetadata` (static)
Create metadata from NBT format.

**Parameters:**
- `tag`: NBT compound

**Returns:**
- SchematicMetadata object

---

## BitArray

Packed long array for efficient storage (internal use).

### Constructor

```python
BitArray(bits_per_entry: int, size: int, data: Optional[List[int]] = None)
```

**Parameters:**
- `bits_per_entry`: Number of bits per value (1-32)
- `size`: Number of entries
- `data`: Optional pre-existing long array

**Raises:**
- `ValueError`: If bits_per_entry is not in range [1, 32]

### Instance Attributes

#### `bits_per_entry: int`
Number of bits used per value.

#### `size: int`
Number of entries in the array.

#### `max_value: int`
Maximum value that can be stored.

#### `data: List[int]`
Backing long array.

### Methods

#### `get(index: int) -> int`
Get value at index.

**Parameters:**
- `index`: Entry index (0-indexed)

**Returns:**
- Value at that index

**Raises:**
- `IndexError`: If index is out of range

**Example:**
```python
value = bit_array.get(42)
```

#### `set(index: int, value: int) -> None`
Set value at index.

**Parameters:**
- `index`: Entry index (0-indexed)
- `value`: Value to set

**Raises:**
- `IndexError`: If index is out of range
- `ValueError`: If value is out of valid range

**Example:**
```python
bit_array.set(42, 7)
```

---

## Type Hints

The library uses type hints for better IDE support:

```python
from typing import Dict, List, Optional, Tuple
from nbt import nbt

# Example function signatures
def create_region(
    name: str,
    position: Tuple[int, int, int],
    size: Tuple[int, int, int]
) -> Region:
    return Region(name, position, size)

def get_block_at(
    region: Region,
    x: int, y: int, z: int
) -> BlockState:
    return region.get_block(x, y, z)
```

---

## Exceptions

### ValueError
Raised when:
- Invalid schematic version
- Missing required NBT tags
- Block position out of bounds
- Invalid BitArray parameters

### FileNotFoundError
Raised when:
- Loading a non-existent file

### IOError
Raised when:
- Cannot write to file
- File is corrupted

### IndexError
Raised when:
- BitArray index out of range

---

## Constants

```python
# From LitematicaSchematic
SCHEMATIC_VERSION = 4
MINECRAFT_DATA_VERSION = 3465
FILE_EXTENSION = ".litematic"

# Common block names
BLOCK_AIR = "minecraft:air"
BLOCK_STONE = "minecraft:stone"
BLOCK_DIRT = "minecraft:dirt"
# ... etc
```

---

## Usage Patterns

### Creating and Saving

```python
from litematica import LitematicaSchematic, Region, BlockState

schematic = LitematicaSchematic()
schematic.metadata.name = "My Build"
schematic.metadata.author = "Player"

region = Region("Main", (0, 0, 0), (10, 10, 10))
stone = BlockState("minecraft:stone")
region.set_block(5, 5, 5, stone)

schematic.add_region(region)
schematic.save("build.litematic")
```

### Loading and Modifying

```python
schematic = LitematicaSchematic.load("build.litematic")
region = list(schematic.regions.values())[0]

diamond = BlockState("minecraft:diamond_block")
region.set_block(0, 0, 0, diamond)

schematic.save("modified.litematic")
```

### Iterating Over Blocks

```python
region = schematic.get_region("Main")
for x in range(region.size[0]):
    for y in range(region.size[1]):
        for z in range(region.size[2]):
            block = region.get_block(x, y, z)
            if block.name != "minecraft:air":
                print(f"Block at ({x},{y},{z}): {block.name}")
```

---

## See Also

- [README.md](README.md) - General documentation
- [EXAMPLES.md](EXAMPLES.md) - Usage examples
- [FORMAT.md](FORMAT.md) - File format specification
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide


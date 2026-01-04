# Quick Start Guide

Get started with the Litematica Python library in 5 minutes!

## Installation

```bash
# Install the NBT library dependency
pip install NBT

# Clone or download this library
cd litematica-python
```

## Your First Schematic

### 1. Create a Simple Structure

```python
from litematica import LitematicaSchematic, Region, BlockState

# Create a new schematic
schematic = LitematicaSchematic()
schematic.metadata.name = "My First Build"
schematic.metadata.author = "YourName"

# Create a region (10x10x10 cube)
region = Region("Main", position=(0, 0, 0), size=(10, 10, 10))

# Fill it with stone
stone = BlockState("minecraft:stone")
for x in range(10):
    for y in range(10):
        for z in range(10):
            region.set_block(x, y, z, stone)

# Add the region and save
schematic.add_region(region)
schematic.save("my_first_build.litematic")
print("Done! Check my_first_build.litematic")
```

### 2. Load and Modify

```python
from litematica import LitematicaSchematic, BlockState

# Load existing schematic
schematic = LitematicaSchematic.load("my_first_build.litematic")

# Get the region
region = list(schematic.regions.values())[0]

# Change the center block to diamond
diamond = BlockState("minecraft:diamond_block")
region.set_block(5, 5, 5, diamond)

# Save with new name
schematic.save("my_modified_build.litematic")
```

### 3. Inspect a Schematic

```python
from litematica import LitematicaSchematic

# Load schematic
schematic = LitematicaSchematic.load("build.litematic")

# Print info
print(f"Name: {schematic.metadata.name}")
print(f"Author: {schematic.metadata.author}")
print(f"Description: {schematic.metadata.description}")
print(f"Number of regions: {len(schematic.regions)}")

# Print region info
for name, region in schematic.regions.items():
    print(f"\nRegion '{name}':")
    print(f"  Size: {region.size}")
    print(f"  Position: {region.position}")
    print(f"  Unique blocks: {len(region.palette)}")
```

## Common Patterns

### Creating a Checkerboard Floor

```python
from litematica import LitematicaSchematic, Region, BlockState

schematic = LitematicaSchematic()
schematic.metadata.name = "Checkerboard"

region = Region("Floor", position=(0, 0, 0), size=(16, 1, 16))

white = BlockState("minecraft:white_wool")
black = BlockState("minecraft:black_wool")

for x in range(16):
    for z in range(16):
        if (x + z) % 2 == 0:
            region.set_block(x, 0, z, white)
        else:
            region.set_block(x, 0, z, black)

schematic.add_region(region)
schematic.save("checkerboard.litematic")
```

### Creating a Hollow Box

```python
from litematica import LitematicaSchematic, Region, BlockState

schematic = LitematicaSchematic()
schematic.metadata.name = "Hollow Box"

region = Region("Box", position=(0, 0, 0), size=(10, 10, 10))

glass = BlockState("minecraft:glass")

for x in range(10):
    for y in range(10):
        for z in range(10):
            # Only place blocks on the edges
            if x == 0 or x == 9 or y == 0 or y == 9 or z == 0 or z == 9:
                region.set_block(x, y, z, glass)

schematic.add_region(region)
schematic.save("hollow_box.litematic")
```

### Using Block Properties

```python
from litematica import BlockState

# Stairs with specific facing
stairs = BlockState("minecraft:oak_stairs", {
    "facing": "north",
    "half": "bottom",
    "shape": "straight",
    "waterlogged": "false"
})

# Door (lower half)
door_lower = BlockState("minecraft:oak_door", {
    "facing": "south",
    "half": "lower",
    "hinge": "left",
    "open": "false",
    "powered": "false"
})

# Door (upper half)
door_upper = BlockState("minecraft:oak_door", {
    "facing": "south",
    "half": "upper",
    "hinge": "left",
    "open": "false",
    "powered": "false"
})

# Use them in your schematic
region.set_block(5, 0, 5, door_lower)
region.set_block(5, 1, 5, door_upper)
```

## Running the Test

Test that everything works:

```bash
python test_basic.py
```

You should see:
```
LITEMATICA PYTHON LIBRARY - BASIC TESTS
✓ Block access test passed!
✓ Palette test passed!
✓ Successfully saved to test_structure.litematic
✓ Successfully loaded
✓ All verifications passed!
✓ ALL TESTS PASSED
```

## Next Steps

1. **Read the [README.md](README.md)** for full API documentation
2. **Check [EXAMPLES.md](EXAMPLES.md)** for more complex examples
3. **Read [FORMAT.md](FORMAT.md)** to understand the file format
4. **Start building!** Create your own schematics

## Common Block IDs

Here are some commonly used block IDs:

### Building Blocks
- `minecraft:stone`
- `minecraft:stone_bricks`
- `minecraft:cobblestone`
- `minecraft:oak_planks`, `minecraft:spruce_planks`, etc.
- `minecraft:bricks`
- `minecraft:glass`
- `minecraft:white_wool` (and other colors)

### Natural Blocks
- `minecraft:dirt`
- `minecraft:grass_block`
- `minecraft:sand`
- `minecraft:gravel`
- `minecraft:oak_log`, `minecraft:spruce_log`, etc.
- `minecraft:oak_leaves`, `minecraft:spruce_leaves`, etc.

### Decorative
- `minecraft:oak_stairs`, `minecraft:stone_stairs`, etc.
- `minecraft:oak_slab`, `minecraft:stone_slab`, etc.
- `minecraft:oak_fence`, `minecraft:glass_pane`, etc.
- `minecraft:torch`, `minecraft:lantern`

### Special
- `minecraft:air` (empty space)
- `minecraft:barrier` (invisible block)
- `minecraft:structure_void` (ignored when pasting)

## Tips

1. **Always reuse BlockState objects** - Don't create a new `BlockState("minecraft:stone")` for every block
2. **Check coordinates** - Make sure x, y, z are within the region size
3. **Use air strategically** - Air blocks (palette ID 0) are the default
4. **Test with small structures first** - Start with 10x10x10 before making huge builds
5. **Save incrementally** - Save your progress as you build

## Troubleshooting

### Import Error
```python
ImportError: No module named 'nbt'
```
**Solution:** Install NBT library: `pip install NBT`

### File Not Found
```python
FileNotFoundError: [Errno 2] No such file or directory: 'file.litematic'
```
**Solution:** Check the file path and make sure the file exists

### Invalid Coordinates
```python
ValueError: Position (10, 10, 10) out of bounds for size (10, 10, 10)
```
**Solution:** Coordinates are 0-indexed. For size (10, 10, 10), valid range is 0-9

## Getting Help

- Check [EXAMPLES.md](EXAMPLES.md) for more examples
- Read [FORMAT.md](FORMAT.md) for format details
- Look at `test_basic.py` for working code examples

Happy building! 🏗️


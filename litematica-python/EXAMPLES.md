# Litematica Python Library - Examples

This document provides detailed examples of using the Litematica Python library.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Creating Structures](#creating-structures)
3. [Working with Block Entities](#working-with-block-entities)
4. [Multi-Region Schematics](#multi-region-schematics)
5. [Modifying Existing Schematics](#modifying-existing-schematics)
6. [Advanced Patterns](#advanced-patterns)

## Basic Usage

### Loading and Inspecting a Schematic

```python
from litematica import LitematicaSchematic

# Load schematic
schematic = LitematicaSchematic.load("castle.litematic")

# Print metadata
print(f"Name: {schematic.metadata.name}")
print(f"Author: {schematic.metadata.author}")
print(f"Description: {schematic.metadata.description}")
print(f"Created: {schematic.metadata.time_created}")
print(f"Regions: {schematic.metadata.region_count}")

# Iterate through regions
for region_name, region in schematic.regions.items():
    print(f"\nRegion: {region_name}")
    print(f"  Position: {region.position}")
    print(f"  Size: {region.size}")
    print(f"  Palette size: {len(region.palette)}")
    print(f"  Block entities: {len(region.block_entities)}")
    print(f"  Entities: {len(region.entities)}")
```

### Analyzing Block Distribution

```python
from collections import Counter

schematic = LitematicaSchematic.load("house.litematic")
region = list(schematic.regions.values())[0]

# Count blocks
block_counts = Counter()
for y in range(region.size[1]):
    for z in range(region.size[2]):
        for x in range(region.size[0]):
            block = region.get_block(x, y, z)
            block_counts[block.name] += 1

# Print top 10 blocks
print("Top 10 most common blocks:")
for block_name, count in block_counts.most_common(10):
    print(f"  {block_name}: {count}")
```

## Creating Structures

### Simple Cube

```python
from litematica import LitematicaSchematic, Region, BlockState

# Create schematic
schematic = LitematicaSchematic()
schematic.metadata.name = "Stone Cube"
schematic.metadata.author = "Builder"
schematic.metadata.description = "A 10x10x10 cube of stone"

# Create region
region = Region("Main", position=(0, 0, 0), size=(10, 10, 10))

# Fill with stone
stone = BlockState("minecraft:stone")
for x in range(10):
    for y in range(10):
        for z in range(10):
            region.set_block(x, y, z, stone)

schematic.add_region(region)
schematic.save("stone_cube.litematic")
```

### Hollow Cube

```python
from litematica import LitematicaSchematic, Region, BlockState

schematic = LitematicaSchematic()
schematic.metadata.name = "Hollow Cube"
schematic.metadata.author = "Builder"

region = Region("Main", position=(0, 0, 0), size=(10, 10, 10))

stone = BlockState("minecraft:stone")
air = BlockState("minecraft:air")

for x in range(10):
    for y in range(10):
        for z in range(10):
            # Set stone on edges, air inside
            if x == 0 or x == 9 or y == 0 or y == 9 or z == 0 or z == 9:
                region.set_block(x, y, z, stone)
            else:
                region.set_block(x, y, z, air)

schematic.add_region(region)
schematic.save("hollow_cube.litematic")
```

### Checkerboard Pattern

```python
from litematica import LitematicaSchematic, Region, BlockState

schematic = LitematicaSchematic()
schematic.metadata.name = "Checkerboard"
schematic.metadata.author = "Builder"

region = Region("Main", position=(0, 0, 0), size=(16, 1, 16))

white_wool = BlockState("minecraft:white_wool")
black_wool = BlockState("minecraft:black_wool")

for x in range(16):
    for z in range(16):
        if (x + z) % 2 == 0:
            region.set_block(x, 0, z, white_wool)
        else:
            region.set_block(x, 0, z, black_wool)

schematic.add_region(region)
schematic.save("checkerboard.litematic")
```

### Simple House

```python
from litematica import LitematicaSchematic, Region, BlockState

schematic = LitematicaSchematic()
schematic.metadata.name = "Simple House"
schematic.metadata.author = "Builder"

region = Region("Main", position=(0, 0, 0), size=(7, 6, 7))

# Materials
oak_planks = BlockState("minecraft:oak_planks")
glass = BlockState("minecraft:glass")
oak_door_lower = BlockState("minecraft:oak_door", {
    "facing": "north", "half": "lower", "hinge": "left", "open": "false"
})
oak_door_upper = BlockState("minecraft:oak_door", {
    "facing": "north", "half": "upper", "hinge": "left", "open": "false"
})
air = BlockState("minecraft:air")

# Floor
for x in range(7):
    for z in range(7):
        region.set_block(x, 0, z, oak_planks)

# Walls
for y in range(1, 5):
    for x in range(7):
        for z in range(7):
            # Walls on edges
            if x == 0 or x == 6 or z == 0 or z == 6:
                # Windows
                if y == 2 and (x == 3 or z == 3) and not (x == 0 or x == 6 and z == 0 or z == 6):
                    region.set_block(x, y, z, glass)
                # Door
                elif z == 0 and x == 3 and y in (1, 2):
                    if y == 1:
                        region.set_block(x, y, z, oak_door_lower)
                    else:
                        region.set_block(x, y, z, oak_door_upper)
                else:
                    region.set_block(x, y, z, oak_planks)
            else:
                region.set_block(x, y, z, air)

# Roof
for x in range(7):
    for z in range(7):
        region.set_block(x, 5, z, oak_planks)

schematic.add_region(region)
schematic.save("simple_house.litematic")
```

### Spiral Staircase

```python
from litematica import LitematicaSchematic, Region, BlockState
import math

schematic = LitematicaSchematic()
schematic.metadata.name = "Spiral Staircase"
schematic.metadata.author = "Builder"

height = 32
radius = 3
region = Region("Main", position=(0, 0, 0), size=(radius*2+1, height, radius*2+1))

stairs_variants = {
    "north": BlockState("minecraft:stone_stairs", {"facing": "north", "half": "bottom", "shape": "straight"}),
    "south": BlockState("minecraft:stone_stairs", {"facing": "south", "half": "bottom", "shape": "straight"}),
    "east": BlockState("minecraft:stone_stairs", {"facing": "east", "half": "bottom", "shape": "straight"}),
    "west": BlockState("minecraft:stone_stairs", {"facing": "west", "half": "bottom", "shape": "straight"}),
}

center_x = radius
center_z = radius

for y in range(height):
    angle = (y / 4) * (2 * math.pi)
    x = int(center_x + radius * math.cos(angle))
    z = int(center_z + radius * math.sin(angle))
    
    # Determine facing based on angle
    facing_angle = angle % (2 * math.pi)
    if facing_angle < math.pi / 4 or facing_angle >= 7 * math.pi / 4:
        facing = "east"
    elif facing_angle < 3 * math.pi / 4:
        facing = "north"
    elif facing_angle < 5 * math.pi / 4:
        facing = "west"
    else:
        facing = "south"
    
    region.set_block(x, y, z, stairs_variants[facing])

schematic.add_region(region)
schematic.save("spiral_staircase.litematic")
```

## Working with Block Entities

### Creating a Chest with Items

```python
from litematica import LitematicaSchematic, Region, BlockState
from nbt import nbt

schematic = LitematicaSchematic()
schematic.metadata.name = "Treasure Chest"
schematic.metadata.author = "Builder"

region = Region("Main", position=(0, 0, 0), size=(1, 1, 1))

# Place chest block
chest_block = BlockState("minecraft:chest", {"facing": "north"})
region.set_block(0, 0, 0, chest_block)

# Create chest data
chest_data = nbt.TAG_Compound()
chest_data.tags.append(nbt.TAG_String(name="id", value="minecraft:chest"))

# Add items
items_list = nbt.TAG_List(name="Items", type=nbt.TAG_Compound)

# Diamond stack
item1 = nbt.TAG_Compound()
item1.tags.append(nbt.TAG_String(name="id", value="minecraft:diamond"))
item1.tags.append(nbt.TAG_Byte(name="Count", value=64))
item1.tags.append(nbt.TAG_Byte(name="Slot", value=0))
items_list.tags.append(item1)

# Gold ingots
item2 = nbt.TAG_Compound()
item2.tags.append(nbt.TAG_String(name="id", value="minecraft:gold_ingot"))
item2.tags.append(nbt.TAG_Byte(name="Count", value=32))
item2.tags.append(nbt.TAG_Byte(name="Slot", value=1))
items_list.tags.append(item2)

chest_data.tags.append(items_list)

# Set block entity
region.set_block_entity(0, 0, 0, chest_data)

schematic.add_region(region)
schematic.save("treasure_chest.litematic")
```

### Creating Signs

```python
from litematica import LitematicaSchematic, Region, BlockState
from nbt import nbt

schematic = LitematicaSchematic()
schematic.metadata.name = "Welcome Sign"
schematic.metadata.author = "Builder"

region = Region("Main", position=(0, 0, 0), size=(1, 2, 1))

# Place sign block
sign_block = BlockState("minecraft:oak_sign", {"rotation": "0"})
region.set_block(0, 0, 0, sign_block)

# Create sign data
sign_data = nbt.TAG_Compound()
sign_data.tags.append(nbt.TAG_String(name="id", value="minecraft:sign"))
sign_data.tags.append(nbt.TAG_String(name="Text1", value='{"text":"Welcome"}'))
sign_data.tags.append(nbt.TAG_String(name="Text2", value='{"text":"to the"}'))
sign_data.tags.append(nbt.TAG_String(name="Text3", value='{"text":"Server!"}'))
sign_data.tags.append(nbt.TAG_String(name="Text4", value='{"text":""}'))

region.set_block_entity(0, 0, 0, sign_data)

schematic.add_region(region)
schematic.save("welcome_sign.litematic")
```

## Multi-Region Schematics

### Building with Multiple Regions

```python
from litematica import LitematicaSchematic, Region, BlockState

schematic = LitematicaSchematic()
schematic.metadata.name = "Castle Complex"
schematic.metadata.author = "Builder"

# Main tower
tower = Region("Tower", position=(0, 0, 0), size=(10, 20, 10))
stone_bricks = BlockState("minecraft:stone_bricks")
for x in range(10):
    for y in range(20):
        for z in range(10):
            if x == 0 or x == 9 or z == 0 or z == 9:
                tower.set_block(x, y, z, stone_bricks)

# Wall
wall = Region("Wall", position=(10, 0, 0), size=(20, 5, 1))
for x in range(20):
    for y in range(5):
        wall.set_block(x, y, 0, stone_bricks)

# Gate
gate = Region("Gate", position=(15, 0, 0), size=(5, 4, 1))
oak_planks = BlockState("minecraft:oak_planks")
for x in range(5):
    for y in range(4):
        gate.set_block(x, y, 0, oak_planks)

# Add all regions
schematic.add_region(tower)
schematic.add_region(wall)
schematic.add_region(gate)

schematic.save("castle_complex.litematic")
```

## Modifying Existing Schematics

### Replacing Blocks

```python
from litematica import LitematicaSchematic, BlockState

# Load existing schematic
schematic = LitematicaSchematic.load("old_build.litematic")
region = list(schematic.regions.values())[0]

# Replace all stone with stone bricks
stone = BlockState("minecraft:stone")
stone_bricks = BlockState("minecraft:stone_bricks")

for x in range(region.size[0]):
    for y in range(region.size[1]):
        for z in range(region.size[2]):
            block = region.get_block(x, y, z)
            if block == stone:
                region.set_block(x, y, z, stone_bricks)

# Update metadata
schematic.metadata.time_modified = int(datetime.now().timestamp() * 1000)

# Save modified schematic
schematic.save("new_build.litematic")
```

### Mirroring a Schematic

```python
from litematica import LitematicaSchematic, Region

def mirror_x(schematic):
    """Mirror schematic along X axis."""
    mirrored = LitematicaSchematic()
    mirrored.metadata = schematic.metadata
    
    for region_name, region in schematic.regions.items():
        new_region = Region(
            region_name,
            region.position,
            region.size
        )
        
        for x in range(region.size[0]):
            for y in range(region.size[1]):
                for z in range(region.size[2]):
                    block = region.get_block(x, y, z)
                    mirrored_x = region.size[0] - 1 - x
                    new_region.set_block(mirrored_x, y, z, block)
        
        mirrored.add_region(new_region)
    
    return mirrored

# Load and mirror
original = LitematicaSchematic.load("build.litematic")
mirrored = mirror_x(original)
mirrored.save("build_mirrored.litematic")
```

### Combining Schematics

```python
from litematica import LitematicaSchematic

# Load multiple schematics
schematic1 = LitematicaSchematic.load("part1.litematic")
schematic2 = LitematicaSchematic.load("part2.litematic")

# Create combined schematic
combined = LitematicaSchematic()
combined.metadata.name = "Combined Build"
combined.metadata.author = "Builder"

# Add regions from both schematics
for region_name, region in schematic1.regions.items():
    combined.add_region(region)

# Offset second schematic
offset_x = 50
for region_name, region in schematic2.regions.items():
    region.position = (
        region.position[0] + offset_x,
        region.position[1],
        region.position[2]
    )
    combined.add_region(region)

combined.save("combined.litematic")
```

## Advanced Patterns

### Generating Circles

```python
from litematica import LitematicaSchematic, Region, BlockState
import math

def create_circle(radius, block_state):
    """Create a circular region."""
    size = radius * 2 + 1
    region = Region("Circle", position=(0, 0, 0), size=(size, 1, size))
    
    center = radius
    for x in range(size):
        for z in range(size):
            dx = x - center
            dz = z - center
            distance = math.sqrt(dx*dx + dz*dz)
            
            if distance <= radius:
                region.set_block(x, 0, z, block_state)
    
    return region

schematic = LitematicaSchematic()
schematic.metadata.name = "Circle Platform"

stone = BlockState("minecraft:stone")
circle = create_circle(10, stone)
schematic.add_region(circle)
schematic.save("circle.litematic")
```

### Generating Spheres

```python
from litematica import LitematicaSchematic, Region, BlockState
import math

def create_sphere(radius, block_state, hollow=False):
    """Create a spherical region."""
    size = radius * 2 + 1
    region = Region("Sphere", position=(0, 0, 0), size=(size, size, size))
    
    center = radius
    for x in range(size):
        for y in range(size):
            for z in range(size):
                dx = x - center
                dy = y - center
                dz = z - center
                distance = math.sqrt(dx*dx + dy*dy + dz*dz)
                
                if hollow:
                    if abs(distance - radius) < 1.0:
                        region.set_block(x, y, z, block_state)
                else:
                    if distance <= radius:
                        region.set_block(x, y, z, block_state)
    
    return region

schematic = LitematicaSchematic()
schematic.metadata.name = "Glass Sphere"

glass = BlockState("minecraft:glass")
sphere = create_sphere(15, glass, hollow=True)
schematic.add_region(sphere)
schematic.save("glass_sphere.litematic")
```

### Parametric Shapes

```python
from litematica import LitematicaSchematic, Region, BlockState
import math

def create_torus(major_radius, minor_radius, block_state):
    """Create a torus (donut shape)."""
    size = (major_radius + minor_radius) * 2 + 1
    region = Region("Torus", position=(0, 0, 0), size=(size, size, size))
    
    center = (major_radius + minor_radius)
    
    for x in range(size):
        for y in range(size):
            for z in range(size):
                dx = x - center
                dy = y - center
                dz = z - center
                
                # Torus equation
                distance_to_center_ring = math.sqrt(dx*dx + dz*dz) - major_radius
                distance_to_tube = math.sqrt(distance_to_center_ring*distance_to_center_ring + dy*dy)
                
                if distance_to_tube <= minor_radius:
                    region.set_block(x, y, z, block_state)
    
    return region

schematic = LitematicaSchematic()
schematic.metadata.name = "Torus"

gold = BlockState("minecraft:gold_block")
torus = create_torus(10, 3, gold)
schematic.add_region(torus)
schematic.save("torus.litematic")
```

### Procedural Terrain

```python
from litematica import LitematicaSchematic, Region, BlockState
import random

def generate_terrain(width, depth, height):
    """Generate simple procedural terrain."""
    region = Region("Terrain", position=(0, 0, 0), size=(width, height, depth))
    
    grass = BlockState("minecraft:grass_block")
    dirt = BlockState("minecraft:dirt")
    stone = BlockState("minecraft:stone")
    
    # Generate height map
    heights = [[random.randint(height//4, height//2) for _ in range(depth)] for _ in range(width)]
    
    for x in range(width):
        for z in range(depth):
            surface_y = heights[x][z]
            
            for y in range(surface_y + 1):
                if y == surface_y:
                    region.set_block(x, y, z, grass)
                elif y >= surface_y - 3:
                    region.set_block(x, y, z, dirt)
                else:
                    region.set_block(x, y, z, stone)
    
    return region

schematic = LitematicaSchematic()
schematic.metadata.name = "Terrain"

terrain = generate_terrain(32, 32, 64)
schematic.add_region(terrain)
schematic.save("terrain.litematic")
```

## Performance Tips

### Batch Block Setting

```python
# SLOW: Setting blocks one at a time with unique states
for x in range(100):
    for y in range(100):
        for z in range(100):
            region.set_block(x, y, z, BlockState("minecraft:stone"))  # Creates new object each time

# FAST: Reuse block state objects
stone = BlockState("minecraft:stone")
for x in range(100):
    for y in range(100):
        for z in range(100):
            region.set_block(x, y, z, stone)
```

### Minimizing Palette Growth

```python
# Pre-create all block states you'll use
blocks = {
    "stone": BlockState("minecraft:stone"),
    "dirt": BlockState("minecraft:dirt"),
    "grass": BlockState("minecraft:grass_block"),
}

# Use them throughout your code
for x in range(size):
    for z in range(size):
        if some_condition:
            region.set_block(x, 0, z, blocks["stone"])
        else:
            region.set_block(x, 0, z, blocks["grass"])
```

## Error Handling

```python
from litematica import LitematicaSchematic

try:
    schematic = LitematicaSchematic.load("file.litematic")
except FileNotFoundError:
    print("Schematic file not found")
except ValueError as e:
    print(f"Invalid schematic format: {e}")
except Exception as e:
    print(f"Error loading schematic: {e}")

# Validate coordinates before setting blocks
region = schematic.get_region("Main")
if region:
    try:
        region.set_block(x, y, z, block_state)
    except ValueError as e:
        print(f"Invalid block position: {e}")
```

## Integration Examples

### Converting from Other Formats

```python
# Placeholder for Schematica to Litematica conversion
def convert_schematica_to_litematica(schematica_file, output_file):
    """Convert .schematic to .litematic format."""
    # Load schematica file (requires schematica parser)
    # ... conversion logic ...
    
    # Create Litematica schematic
    schematic = LitematicaSchematic()
    # ... populate regions ...
    
    schematic.save(output_file)
```

### Exporting Block Lists

```python
from collections import Counter

def export_block_list(schematic_file, output_file):
    """Export list of blocks and counts."""
    schematic = LitematicaSchematic.load(schematic_file)
    
    total_counts = Counter()
    for region in schematic.regions.values():
        for x in range(region.size[0]):
            for y in range(region.size[1]):
                for z in range(region.size[2]):
                    block = region.get_block(x, y, z)
                    if block.name != "minecraft:air":
                        total_counts[block.name] += 1
    
    with open(output_file, 'w') as f:
        f.write("Block,Count\n")
        for block_name, count in sorted(total_counts.items()):
            f.write(f"{block_name},{count}\n")

export_block_list("build.litematic", "blocks.csv")
```


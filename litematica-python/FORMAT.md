# Litematica File Format Documentation

## Overview

Litematica (.litematic) is a schematic file format used in Minecraft for storing and recreating structures. It uses the NBT (Named Binary Tag) format with GZIP compression.

## File Structure

### Top-Level Structure

A Litematica file is a compressed NBT file with the following root structure:

```
ROOT (TAG_Compound)
├── Version (TAG_Int): Schema version (currently 4)
├── MinecraftDataVersion (TAG_Int): Minecraft data version
├── Metadata (TAG_Compound): Schematic metadata
└── Regions (TAG_Compound): Named regions containing block data
```

## Metadata Structure

The Metadata compound contains information about the schematic:

```
Metadata (TAG_Compound)
├── Name (TAG_String): Schematic name
├── Author (TAG_String): Creator's name
├── Description (TAG_String): Schematic description
├── RegionCount (TAG_Int): Number of regions (optional)
├── TotalVolume (TAG_Long): Total volume in blocks (optional)
├── TotalBlocks (TAG_Long): Total non-air blocks (optional)
├── TimeCreated (TAG_Long): Creation timestamp (milliseconds)
├── TimeModified (TAG_Long): Last modification timestamp (milliseconds)
├── EnclosingSize (TAG_Compound): Overall dimensions
│   ├── x (TAG_Int)
│   ├── y (TAG_Int)
│   └── z (TAG_Int)
└── PreviewImageData (TAG_Int_Array): Preview image pixels (optional)
```

### Preview Image

The PreviewImageData is an integer array containing ARGB pixel data. The image dimensions are not stored in the format but are typically 140x140 pixels.

## Regions Structure

The Regions compound contains one or more named sub-regions. Each region is stored as:

```
Regions (TAG_Compound)
└── [RegionName] (TAG_Compound)
    ├── Position (TAG_Compound): Relative position
    │   ├── x (TAG_Int)
    │   ├── y (TAG_Int)
    │   └── z (TAG_Int)
    ├── Size (TAG_Compound): Dimensions
    │   ├── x (TAG_Int)
    │   ├── y (TAG_Int)
    │   └── z (TAG_Int)
    ├── BlockStatePalette (TAG_List of TAG_Compound): Unique block states
    ├── BlockStates (TAG_Long_Array): Packed block indices
    ├── TileEntities (TAG_List of TAG_Compound): Block entities (optional)
    ├── Entities (TAG_List of TAG_Compound): Entities (optional)
    └── PendingBlockTicks (TAG_List of TAG_Compound): Scheduled ticks (optional)
```

## Block State Palette

The BlockStatePalette is a list of unique block states used in the region. Each entry is a TAG_Compound containing:

```
BlockStatePalette[i] (TAG_Compound)
├── Name (TAG_String): Block ID (e.g., "minecraft:stone")
└── Properties (TAG_Compound): Block properties (optional)
    └── [property_name] (TAG_String): property value
```

### Example Palette Entries

**Simple Block (no properties):**
```
{
  Name: "minecraft:stone"
}
```

**Block with Properties:**
```
{
  Name: "minecraft:oak_stairs",
  Properties: {
    facing: "north",
    half: "bottom",
    shape: "straight",
    waterlogged: "false"
  }
}
```

## Block States Storage

The BlockStates tag contains a TAG_Long_Array that stores indices into the BlockStatePalette using a packed bit array.

### Bit Packing Algorithm

1. **Bits Per Entry**: Calculated as `max(2, ceil(log2(palette_size)))`
   - Minimum 2 bits per entry
   - Maximum 32 bits per entry
   - Example: palette with 5 entries needs 3 bits per entry

2. **Storage Layout**:
   - Blocks are stored in YZX order (Y varies slowest, X varies fastest)
   - Block index: `index = y * (size_x * size_z) + z * size_x + x`
   - Multiple block indices are packed into each long value (64 bits)

3. **Packing Details**:
   - Values are packed from LSB to MSB within each long
   - A single block index may span across two consecutive longs
   - The long array length is: `ceil((volume * bits_per_entry) / 64)`

### Example

For a 2x2x2 region with 3 block types:
- Volume: 8 blocks
- Palette size: 3 (needs 2 bits per entry)
- Storage: 8 blocks × 2 bits = 16 bits = 1 long (with 48 unused bits)

Block order in array (YZX):
```
Index | Y | Z | X | Palette ID
------|---|---|---|------------
  0   | 0 | 0 | 0 |     0
  1   | 0 | 0 | 1 |     1
  2   | 0 | 1 | 0 |     2
  3   | 0 | 1 | 1 |     0
  4   | 1 | 0 | 0 |     1
  5   | 1 | 0 | 1 |     2
  6   | 1 | 1 | 0 |     0
  7   | 1 | 1 | 1 |     1
```

Packed in long (LSB first):
```
bits:  [1][0][2][0][1][2][0][1] = 0b01_00_10_00_01_10_00_01
```

## Block Entities (TileEntities)

Block entities (formerly called tile entities) store additional data for blocks like chests, signs, etc.

```
TileEntities[i] (TAG_Compound)
├── x (TAG_Int): X position (relative to region)
├── y (TAG_Int): Y position (relative to region)
├── z (TAG_Int): Z position (relative to region)
├── id (TAG_String): Entity ID (e.g., "minecraft:chest")
└── [entity_data]: Additional entity-specific NBT data
```

### Common Block Entities

**Chest:**
```
{
  x: 5, y: 10, z: 3,
  id: "minecraft:chest",
  Items: [
    {Slot: 0b, id: "minecraft:diamond", Count: 64b},
    ...
  ]
}
```

**Sign:**
```
{
  x: 2, y: 64, z: 8,
  id: "minecraft:sign",
  Text1: '{"text":"Hello"}',
  Text2: '{"text":"World"}',
  Text3: '{"text":""}',
  Text4: '{"text":""}'
}
```

## Entities

Entities store mobs, item frames, armor stands, and other non-block objects.

```
Entities[i] (TAG_Compound)
├── Pos (TAG_List of TAG_Double): Position (relative to region)
│   ├── [0]: X position (TAG_Double)
│   ├── [1]: Y position (TAG_Double)
│   └── [2]: Z position (TAG_Double)
├── id (TAG_String): Entity ID (e.g., "minecraft:cow")
└── [entity_data]: Additional entity-specific NBT data
```

### Example Entity

**Armor Stand:**
```
{
  Pos: [5.5d, 64.0d, 3.5d],
  id: "minecraft:armor_stand",
  Rotation: [45.0f, 0.0f],
  NoGravity: 1b,
  ShowArms: 1b,
  Small: 0b
}
```

## Pending Block Ticks

Scheduled block updates (e.g., for water flow, redstone).

```
PendingBlockTicks[i] (TAG_Compound)
├── x (TAG_Int): X position (relative to region)
├── y (TAG_Int): Y position (relative to region)
├── z (TAG_Int): Z position (relative to region)
├── Block (TAG_String): Block ID
├── Time (TAG_Int): Delay in ticks (relative)
└── Priority (TAG_Int): Priority (default 0)
```

### Example

```
{
  x: 10, y: 64, z: 5,
  Block: "minecraft:water",
  Time: 5,
  Priority: 0
}
```

## Version History

### Version 4 (Current)
- Current stable version
- Supports multiple sub-regions
- Includes pending block ticks

### Version 3
- Added PendingBlockTicks support
- Improved entity storage

### Version 2
- Changed entity and tile entity storage format
- Position data moved into entity NBT

### Version 1
- Initial Litematica format
- Basic region support

## Coordinate Systems

### Schematic Coordinates
- **Origin**: Arbitrary point defined when creating the schematic
- **Regions**: Each region has a position relative to the schematic origin
- **Blocks**: Block positions within each region (0,0,0) to (size_x-1, size_y-1, size_z-1)

### World Placement
When placing a schematic in the world, the schematic origin maps to a world coordinate, and all regions are offset from that point.

## Special Blocks

### Air Blocks
- Air is typically assigned palette ID 0
- Air blocks don't require block entities
- Air is not counted in TotalBlocks metadata

### Invisible/Technical Blocks
- Barrier blocks: `minecraft:barrier`
- Structure void: `minecraft:structure_void` (ignored when pasting)
- Light blocks: `minecraft:light`

## Multi-Region Schematics

Litematica supports multiple independent regions in a single file:

```
Regions:
  - "Main Building"
  - "Garden"
  - "Pathway"
```

Each region:
- Has its own position relative to the schematic origin
- Has independent block storage and palette
- Can overlap with other regions
- Can be toggled on/off during placement

## Data Version

The MinecraftDataVersion tag corresponds to Minecraft's internal data version, which changes with each release. This is used for automatic upgrading of block IDs and entity data when loading in newer Minecraft versions.

### Common Data Versions
- 1.12.2: 1343
- 1.13.2: 1631
- 1.14.4: 1976
- 1.15.2: 2230
- 1.16.5: 2586
- 1.17.1: 2730
- 1.18.2: 2975
- 1.19.2: 3120
- 1.20.1: 3465

## Implementation Notes

### Reading Algorithm

1. Read and decompress the GZIP NBT file
2. Verify Version tag (should be ≤ 4)
3. Read Metadata
4. For each region:
   a. Read Position and Size
   b. Read BlockStatePalette
   c. Calculate bits_per_entry from palette size
   d. Unpack BlockStates long array
   e. Map each block position to its palette entry
   f. Read TileEntities, Entities, and PendingBlockTicks

### Writing Algorithm

1. Create metadata with current timestamp
2. For each region:
   a. Scan all blocks and build palette
   b. Assign palette IDs (0 = air)
   c. Calculate bits_per_entry
   d. Pack block indices into long array
   e. Write Position, Size, BlockStatePalette, BlockStates
   f. Write TileEntities, Entities, PendingBlockTicks
3. Write root structure
4. Compress with GZIP

### Performance Considerations

- **Memory**: Large schematics can use significant memory due to unpacked block data
- **Palette**: Smaller palettes = more efficient storage
- **Air optimization**: Use palette ID 0 for air to minimize storage
- **Bit packing**: Efficient for regions with few unique blocks

## Compatibility

### With Other Formats

**Schematica (.schematic)**
- Older format, single region only
- Uses TAG_Byte_Array for block storage
- Limited to 256 block types per schematic

**Sponge Schematic (.schem)**
- Similar NBT structure
- Different block storage format (varint array)
- Single region

**Vanilla Structure (.nbt)**
- Minecraft's native structure format
- Different block storage (palette + list)
- Single structure, no metadata

## Best Practices

1. **Always use Version 4** for new schematics
2. **Set metadata** appropriately (name, author, description)
3. **Use structure voids** for air blocks that should not overwrite existing blocks
4. **Minimize palette size** by removing duplicate block states
5. **Compress efficiently** by grouping similar blocks together
6. **Include preview images** for better user experience
7. **Set timestamps** to track schematic age
8. **Validate data** when reading to handle corrupted files gracefully

## Tools and Libraries

### Java
- **Litematica**: The reference implementation (Minecraft mod)
- **malilib**: Utility library used by Litematica

### Python
- **litematica-python**: This library
- **NBT library**: For reading/writing NBT data

### Other
- **NBTExplorer**: View and edit NBT files manually
- **MCEdit**: World editor with schematic support (Schematica format)

## Error Handling

### Common Issues

1. **Corrupted GZIP**: File may be truncated or damaged
2. **Invalid Version**: Unsupported version number
3. **Missing Required Tags**: Metadata or Regions missing
4. **Invalid Palette Size**: Mismatch between palette and block states
5. **Out of Bounds**: Block entity/entity positions outside region bounds
6. **Invalid Block States**: Unknown block IDs or invalid properties

### Validation Checks

- Version is between 1 and 4
- All required tags present
- Region sizes are positive
- BlockStates array length matches expected
- Palette size matches bits_per_entry
- All block indices < palette size
- Entity/block entity positions within region bounds

## Future Extensions

Potential future enhancements:
- Version 5 with improved compression
- Built-in support for custom blocks/mods
- Metadata for schematic tags/categories
- Multi-version compatibility data
- Embedded transformation data (rotation, mirroring)
- Schematic dependencies and linking

## References

- [Litematica GitHub Repository](https://github.com/maruohon/litematica)
- [NBT Format Specification](https://minecraft.fandom.com/wiki/NBT_format)
- [Minecraft Data Versions](https://minecraft.fandom.com/wiki/Data_version)


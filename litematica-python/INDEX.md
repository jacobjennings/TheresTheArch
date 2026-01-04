# Litematica Python Library - Documentation Index

Welcome to the Litematica Python Library documentation! This index will help you find the information you need.

## 📚 Documentation Structure

### For Getting Started

1. **[QUICKSTART.md](QUICKSTART.md)** - Start here!
   - Installation instructions
   - Your first schematic in 5 minutes
   - Common patterns
   - Troubleshooting

2. **[README.md](README.md)** - Overview and basics
   - Features overview
   - Installation
   - Quick examples
   - Basic API usage

### For Learning by Example

3. **[EXAMPLES.md](EXAMPLES.md)** - Comprehensive examples
   - Basic usage patterns
   - Creating structures (cubes, houses, spirals)
   - Working with block entities
   - Multi-region schematics
   - Modifying existing schematics
   - Advanced patterns (circles, spheres, procedural generation)

### For Reference

4. **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation
   - All classes and methods
   - Parameter descriptions
   - Return types and exceptions
   - Usage examples

5. **[FORMAT.md](FORMAT.md)** - File format specification
   - Complete NBT structure
   - Block state palette format
   - Bit packing algorithm
   - Version history
   - Compatibility information

### For Contributing

6. **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
   - Development setup
   - Code style
   - Testing requirements
   - Pull request process

## 🎯 Quick Navigation

### I want to...

#### Learn the basics
→ Start with [QUICKSTART.md](QUICKSTART.md)

#### See code examples
→ Check [EXAMPLES.md](EXAMPLES.md)

#### Look up a specific function
→ See [API_REFERENCE.md](API_REFERENCE.md)

#### Understand the file format
→ Read [FORMAT.md](FORMAT.md)

#### Report a bug or request a feature
→ Follow [CONTRIBUTING.md](CONTRIBUTING.md)

#### Create a simple schematic
→ [QUICKSTART.md - Your First Schematic](QUICKSTART.md#your-first-schematic)

#### Load and modify a schematic
→ [QUICKSTART.md - Load and Modify](QUICKSTART.md#2-load-and-modify)

#### Work with block entities (chests, signs)
→ [EXAMPLES.md - Working with Block Entities](EXAMPLES.md#working-with-block-entities)

#### Create complex shapes
→ [EXAMPLES.md - Advanced Patterns](EXAMPLES.md#advanced-patterns)

#### Understand block properties
→ [QUICKSTART.md - Using Block Properties](QUICKSTART.md#using-block-properties)

#### Convert between formats
→ [EXAMPLES.md - Integration Examples](EXAMPLES.md#integration-examples)

## 📖 Documentation by Topic

### Core Concepts

| Topic | Where to Find It |
|-------|------------------|
| Block states | [QUICKSTART.md](QUICKSTART.md#using-block-properties) |
| Regions | [API_REFERENCE.md - Region](API_REFERENCE.md#region) |
| Metadata | [API_REFERENCE.md - SchematicMetadata](API_REFERENCE.md#schematicmetadata) |
| Palette | [FORMAT.md - Block State Palette](FORMAT.md#block-state-palette) |
| Bit packing | [FORMAT.md - Block States Storage](FORMAT.md#block-states-storage) |

### Common Tasks

| Task | Where to Find It |
|------|------------------|
| Create a schematic | [QUICKSTART.md](QUICKSTART.md#1-create-a-simple-structure) |
| Load a schematic | [QUICKSTART.md](QUICKSTART.md#2-load-and-modify) |
| Set blocks | [API_REFERENCE.md - Region.set_block](API_REFERENCE.md#set_blockx-int-y-int-z-int-state-blockstate---none) |
| Get blocks | [API_REFERENCE.md - Region.get_block](API_REFERENCE.md#get_blockx-int-y-int-z-int---blockstate) |
| Add block entities | [EXAMPLES.md - Creating a Chest](EXAMPLES.md#creating-a-chest-with-items) |
| Multiple regions | [EXAMPLES.md - Multi-Region Schematics](EXAMPLES.md#multi-region-schematics) |

### Advanced Topics

| Topic | Where to Find It |
|-------|------------------|
| Performance optimization | [EXAMPLES.md - Performance Tips](EXAMPLES.md#performance-tips) |
| Error handling | [EXAMPLES.md - Error Handling](EXAMPLES.md#error-handling) |
| Procedural generation | [EXAMPLES.md - Procedural Terrain](EXAMPLES.md#procedural-terrain) |
| Format internals | [FORMAT.md](FORMAT.md) |

## 🔍 API Quick Reference

### Main Classes

```python
from litematica import (
    LitematicaSchematic,  # Main schematic class
    Region,               # Region within schematic
    BlockState,           # Block type with properties
    SchematicMetadata,    # Schematic metadata
    BitArray,             # Internal storage (advanced)
)
```

### Common Block IDs

See [QUICKSTART.md - Common Block IDs](QUICKSTART.md#common-block-ids) for a list of frequently used block identifiers.

### File Format Versions

| Version | Support | Notes |
|---------|---------|-------|
| 4 | ✅ Full | Current version |
| 3 | ✅ Read | Legacy support |
| 2 | ✅ Read | Legacy support |
| 1 | ✅ Read | Legacy support |

## 🧪 Testing

Run the test suite:
```bash
python test_basic.py
```

See [test_basic.py](test_basic.py) for test implementation.

## 📦 Files in This Library

```
litematica-python/
├── __init__.py              # Package initialization
├── litematica.py            # Main library code
├── test_basic.py            # Test suite
├── setup.py                 # Installation setup
├── requirements.txt         # Dependencies
│
├── README.md                # Main documentation
├── QUICKSTART.md            # Quick start guide
├── EXAMPLES.md              # Usage examples
├── API_REFERENCE.md         # Complete API docs
├── FORMAT.md                # File format spec
├── CONTRIBUTING.md          # Contribution guide
└── INDEX.md                 # This file
```

## 🔗 External Resources

- [Litematica Mod GitHub](https://github.com/maruohon/litematica) - Reference implementation
- [NBT Format Wiki](https://minecraft.fandom.com/wiki/NBT_format) - NBT specification
- [Minecraft Wiki](https://minecraft.fandom.com) - Block IDs and properties
- [Data Versions](https://minecraft.fandom.com/wiki/Data_version) - Minecraft version mapping

## 💡 Tips for Learning

1. **Start Small**: Begin with [QUICKSTART.md](QUICKSTART.md) and create a simple cube
2. **Run Tests**: Execute `test_basic.py` to see working examples
3. **Experiment**: Modify examples from [EXAMPLES.md](EXAMPLES.md)
4. **Read Code**: The library is ~400 lines of well-commented Python
5. **Check Format**: When in doubt, refer to [FORMAT.md](FORMAT.md)

## ⚡ Common Gotchas

1. **Coordinates are 0-indexed**: A 10×10×10 region has coordinates 0-9
2. **Reuse BlockState objects**: Don't create new ones for every block
3. **Air is ID 0**: The palette always has air at index 0
4. **Properties are strings**: Block properties are always string→string maps
5. **Positions are tuples**: Use `(x, y, z)` not `[x, y, z]`

## 📝 Version Information

- **Library Version**: 1.0.0
- **Schematic Format Version**: 4
- **Target Minecraft Version**: 1.20.1 (data version 3465)
- **Python Requirement**: 3.7+

## 🆘 Getting Help

1. Check this documentation
2. Run the test script: `python test_basic.py`
3. Look at working examples in [EXAMPLES.md](EXAMPLES.md)
4. Read the source code (it's well commented!)
5. Open an issue on GitHub

## 🎉 Ready to Build!

Pick your starting point:
- **New to Litematica?** → [QUICKSTART.md](QUICKSTART.md)
- **Want to see examples?** → [EXAMPLES.md](EXAMPLES.md)
- **Need API details?** → [API_REFERENCE.md](API_REFERENCE.md)
- **Curious about format?** → [FORMAT.md](FORMAT.md)

Happy building! 🏗️


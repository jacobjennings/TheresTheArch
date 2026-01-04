# TheresTheArch

A project for generating Minecraft schematics using Litematica, starting with the Saint Louis Arch.

## Project Structure

```
TheresTheArch/
├── litematica/              # Git submodule: Litematica mod source (Java)
└── litematica-python/       # Python library for Litematica format
    ├── litematica.py        # Main library implementation
    ├── __init__.py          # Package initialization
    ├── test_basic.py        # Test suite
    ├── setup.py             # Installation setup
    ├── requirements.txt     # Python dependencies
    │
    └── Documentation/
        ├── README.md        # Main library documentation
        ├── INDEX.md         # Documentation index
        ├── QUICKSTART.md    # Quick start guide
        ├── EXAMPLES.md      # Comprehensive examples
        ├── API_REFERENCE.md # Complete API documentation
        ├── FORMAT.md        # File format specification
        └── CONTRIBUTING.md  # Contribution guidelines
```

## Litematica Python Library

A comprehensive Python library for reading, writing, and manipulating Litematica schematic files (.litematic).

### Features

- ✅ Full support for Litematica format (versions 1-4)
- ✅ Read and write .litematic files
- ✅ Multiple regions per schematic
- ✅ Block states with properties
- ✅ Block entities (chests, signs, etc.)
- ✅ Entities (mobs, armor stands, etc.)
- ✅ Pending block ticks
- ✅ Efficient bit-packed storage
- ✅ Extensive documentation

### Quick Start

```python
from litematica import LitematicaSchematic, Region, BlockState

# Create a new schematic
schematic = LitematicaSchematic()
schematic.metadata.name = "My Build"
schematic.metadata.author = "Builder"

# Create a region
region = Region("Main", position=(0, 0, 0), size=(10, 10, 10))

# Add blocks
stone = BlockState("minecraft:stone")
for x in range(10):
    for y in range(10):
        for z in range(10):
            region.set_block(x, y, z, stone)

# Save
schematic.add_region(region)
schematic.save("my_build.litematic")
```

### Documentation

The library includes extensive documentation:

- **[QUICKSTART.md](litematica-python/QUICKSTART.md)** - Get started in 5 minutes
- **[README.md](litematica-python/README.md)** - Library overview and features
- **[EXAMPLES.md](litematica-python/EXAMPLES.md)** - Comprehensive usage examples
- **[API_REFERENCE.md](litematica-python/API_REFERENCE.md)** - Complete API documentation
- **[FORMAT.md](litematica-python/FORMAT.md)** - Detailed file format specification
- **[INDEX.md](litematica-python/INDEX.md)** - Documentation index and navigation

### Installation

```bash
cd litematica-python
pip install -r requirements.txt
```

### Running Tests

```bash
cd litematica-python
python test_basic.py
```

## Format Documentation

The library includes comprehensive documentation of the Litematica file format:

- Complete NBT structure
- Block state palette system
- Bit packing algorithm
- Block entities and entities
- Version history and compatibility
- Implementation notes

See [FORMAT.md](litematica-python/FORMAT.md) for details.

## Dependencies

- Python 3.7+
- NBT library (`pip install NBT`)

## Gateway Arch Generator

The **theresthearch** directory contains a complete application for generating Gateway Arch schematics.

### Quick Setup

```bash
cd TheresTheArch
./setup.sh              # Run setup (creates venv, installs dependencies)
source venv/bin/activate  # Activate virtual environment
```

### Usage

```bash
# Interactive CLI (recommended, no GUI dependencies)
python theresthearch/arch_cli.py

# GUI (requires tkinter)
python theresthearch/arch_gui.py

# Or use Python API directly
python -c "from theresthearch import create_simple_arch; create_simple_arch(scale=0.5)"
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

### Features

- 🏛️ **Mathematically Accurate**: Uses the real Gateway Arch catenary equation
- 🎚️ **Scalable**: From 50 blocks to 1000+ blocks tall
- 🎨 **Customizable**: Choose block types, hollow/solid, wall thickness
- 🖥️ **GUI Interface**: Easy-to-use graphical application
- 📊 **Live Preview**: View dimensions and block counts before generating
- ⚡ **Progress Tracking**: Real-time generation progress

### Quick Start

```python
from theresthearch import ArchGenerator

# Create generator with custom options
generator = ArchGenerator(
    scale=0.5,           # 315 blocks tall
    hollow=True,         # Hollow interior
    thickness=3,         # 3-block thick walls
    primary_block="minecraft:quartz_block",
    corner_block="minecraft:quartz_pillar"
)

# Generate schematic
schematic = generator.generate()
schematic.save("gateway_arch.litematic")
```

See [theresthearch/README.md](theresthearch/README.md) for detailed documentation.

## Project Goals

1. ✅ Understand the Litematica file format
2. ✅ Create a Python library for reading/writing .litematic files
3. ✅ Document the format extensively
4. ✅ Generate procedural structures (Gateway Arch complete!)

## References

- [Litematica Mod](https://github.com/maruohon/litematica) - Reference implementation
- [NBT Format](https://minecraft.fandom.com/wiki/NBT_format) - NBT specification
- [Minecraft Wiki](https://minecraft.fandom.com) - Block IDs and properties

## License

See LICENSE file for details.

## Credits

Format documentation and library implementation based on the Litematica mod by maruohon.

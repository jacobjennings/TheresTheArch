# TheresTheArch

A project for generating Minecraft schematics using Litematica, starting with the Saint Louis (Gateway) Arch.

## AI Disclosure

This project was developed with substantial assistance from AI coding tools.
AI was used to help write the Litematica format library,
the arch-generation algorithm, and the documentation in this repository. All
code has been reviewed and exercised by the author (the test suite and a smoke
generation run in CI), but please treat it accordingly and report anything that
looks off.

## Project Structure

```
TheresTheArch/
├── litematica/              # Git submodule: upstream Litematica mod (reference only, optional)
├── litematica-python/       # Python library for the .litematic format
│   ├── litematica.py        # Main library implementation
│   ├── __init__.py          # Package initialization
│   ├── test_basic.py        # Test suite
│   ├── setup.py             # Installation setup
│   ├── requirements.txt     # Python dependencies
│   └── *.md                 # Library docs (README, QUICKSTART, EXAMPLES, API_REFERENCE, FORMAT, FEATURES, INDEX, CONTRIBUTING)
│
├── theresthearch/           # Gateway Arch generator application
│   ├── arch_generator.py    # Core generation logic + Python API
│   ├── arch_cli.py          # Interactive command-line interface
│   ├── arch_gui.py          # Tkinter GUI
│   ├── __init__.py          # Package init
│   └── README.md            # Generator docs and design notes
│
├── INSTALL.md               # Installation guide
├── USAGE_GUIDE.md           # Usage guide
├── CHANGELOG.md             # Version history
└── setup.sh                 # One-step environment setup
```

> The `litematica/` submodule is only a pointer to the upstream
> [maruohon/litematica](https://github.com/maruohon/litematica) mod (LGPL-3.0)
> for reference. It is **not required** to use this project — clone without
> `--recursive` if you don't need it.

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

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file.

The `litematica-python` library is an independent, from-scratch Python
implementation of the `.litematic` file format. File formats themselves are not
copyrightable; no code from the upstream mod is copied or redistributed here.

## Credits

- File-format understanding and naming derived from the
  [Litematica mod](https://github.com/maruohon/litematica) by **maruohon**,
  which is licensed under the GNU LGPL-3.0. The mod is referenced (as an
  optional git submodule) but not redistributed.
- Gateway Arch designed by **Eero Saarinen** (completed 1965). Catenary
  coefficients via [Wikipedia](https://en.wikipedia.org/wiki/Gateway_Arch).

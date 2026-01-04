# TheresTheArch - Gateway Arch Generator

Generate Minecraft schematics of the iconic Gateway Arch in St. Louis using its actual mathematical equation.

![Gateway Arch](https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/St_Louis_night_expblend_cropped.jpg/320px-St_Louis_night_expblend_cropped.jpg)

## Overview

This project generates accurate Minecraft schematics of the [Gateway Arch](https://en.wikipedia.org/wiki/Gateway_Arch) using the weighted catenary equation that defines its actual shape:

**y = 693.8597 - 68.7672 × cosh(0.0100333 × x)**

## Features

- ✅ **Mathematically Accurate**: Uses the real Gateway Arch equation
- ✅ **Customizable Scale**: Generate from small (50 blocks) to massive (1000+ blocks)
- ✅ **Hollow or Solid**: Choose between hollow (efficient) or solid construction
- ✅ **Block Customization**: Select primary and corner block types
- ✅ **GUI Application**: Easy-to-use graphical interface
- ✅ **Live Preview**: See dimensions and block counts before generating
- ✅ **Progress Tracking**: Real-time generation progress

## Installation

### Prerequisites

1. Python 3.7 or higher
2. NBT library

### Setup

```bash
cd TheresTheArch
pip install -r theresthearch/requirements.txt
```

**Note for Linux users:** The GUI requires tkinter. Install it with:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

If you can't install tkinter, use the command-line interface instead (see below).

## Usage

### Command Line Interface (No GUI Required)

Interactive command-line interface with guided setup:

```bash
python theresthearch/arch_cli.py
```

Features:
- Quick presets (small, medium, large, full scale)
- Custom settings with prompts
- Live preview of dimensions and block counts
- Progress tracking
- No GUI dependencies

### GUI Application

Launch the graphical interface (requires tkinter):

```bash
python theresthearch/arch_gui.py
```

The GUI provides:
- **Scale slider**: Adjust arch size (0.1x to 2.0x)
- **Hollow option**: Choose hollow or solid construction
- **Wall thickness**: Set thickness for hollow arches (1-10 blocks)
- **Block selection**: Choose primary and corner blocks
- **Live preview**: View dimensions and estimated block counts
- **File browser**: Select output location

### Command Line

Generate a simple arch programmatically:

```python
from theresthearch import create_simple_arch

# Generate a medium-sized hollow arch
create_simple_arch(
    scale=0.5,  # 315 blocks tall
    output_file="gateway_arch.litematic"
)
```

### Advanced Usage

```python
from theresthearch import ArchGenerator

# Create custom generator
generator = ArchGenerator(
    scale=0.75,  # 472 blocks tall
    hollow=True,
    thickness=5,
    primary_block="minecraft:quartz_block",
    corner_block="minecraft:quartz_pillar"
)

# Get dimensions
dims = generator.calculate_dimensions()
print(f"Overall: {dims['overall']}")
print(f"Base: {dims['base']}")
print(f"Peak: {dims['peak']}")

# Estimate blocks
blocks = generator.estimate_blocks()
for block_type, count in blocks.items():
    print(f"{block_type}: {count:,}")

# Generate with progress callback
def progress(current, total, message):
    print(f"{message} {current}/{total}")

schematic = generator.generate(progress_callback=progress)
schematic.save("custom_arch.litematic")
```

## Scale Guide

| Scale | Height (blocks) | Width (blocks) | Best For |
|-------|----------------|----------------|----------|
| 0.1   | 63             | 63             | Testing, small builds |
| 0.25  | 158            | 158            | Compact servers |
| 0.5   | 315            | 315            | Standard size |
| 0.75  | 472            | 472            | Large servers |
| 1.0   | 630            | 630            | Full scale (massive!) |
| 2.0   | 1260           | 1260           | Epic builds |

**Note**: Larger scales require significantly more blocks and generation time!

## Block Recommendations

### Recommended Combinations

**Modern/Clean:**
- Primary: `minecraft:white_concrete`
- Corner: `minecraft:light_gray_concrete`

**Classic:**
- Primary: `minecraft:quartz_block`
- Corner: `minecraft:quartz_pillar`

**Metallic:**
- Primary: `minecraft:iron_block`
- Corner: `minecraft:dark_oak_log`

**Futuristic:**
- Primary: `minecraft:prismarine`
- Corner: `minecraft:sea_lantern`

**Stone:**
- Primary: `minecraft:stone_bricks`
- Corner: `minecraft:chiseled_stone_bricks`

## Mathematical Background

The Gateway Arch is a **weighted catenary arch**, designed by architect Eero Saarinen. The shape is defined by the equation:

```
y = A - B × cosh(C × x)
```

Where:
- A = 693.8597 feet
- B = 68.7672 feet
- C = 0.0100333

The actual arch is:
- **Height**: 630 feet (192 meters)
- **Width at base**: 630 feet (192 meters)
- **Construction**: Stainless steel exterior, carbon steel interior

This generator converts these dimensions to Minecraft blocks, maintaining the exact proportions.

## Architecture

```
theresthearch/
├── __init__.py          # Package initialization
├── arch_generator.py    # Core generation logic
├── arch_gui.py          # GUI application
├── requirements.txt     # Dependencies
└── README.md           # This file
```

### Core Components

**ArchGenerator Class:**
- `catenary(x)`: Calculate y-coordinate from catenary equation
- `get_arch_y(x, z)`: Get height at given position
- `should_place_block()`: Determine block placement
- `calculate_dimensions()`: Get arch dimensions
- `estimate_blocks()`: Estimate block counts
- `generate()`: Generate the schematic

## Examples

### Small Test Arch

```python
from theresthearch import create_simple_arch

create_simple_arch(scale=0.2, output_file="test_arch.litematic")
```

Output:
- Height: 126 blocks
- Width: 126 blocks
- ~50,000 blocks
- Generation time: ~30 seconds

### Medium Arch (Recommended)

```python
from theresthearch import create_simple_arch

create_simple_arch(scale=0.5, output_file="medium_arch.litematic")
```

Output:
- Height: 315 blocks
- Width: 315 blocks
- ~300,000 blocks
- Generation time: ~5 minutes

### Full Scale Arch

```python
from theresthearch import ArchGenerator

generator = ArchGenerator(
    scale=1.0,
    hollow=True,
    thickness=5,
    primary_block="minecraft:quartz_block",
    corner_block="minecraft:quartz_pillar"
)

schematic = generator.generate()
schematic.save("full_scale_arch.litematic")
```

Output:
- Height: 630 blocks
- Width: 630 blocks
- ~2,000,000 blocks
- Generation time: ~30 minutes

## Known Limitations

**Manual Cleanup at Peak**: The generated arch may have minor "sawtooth" artifacts near the very top where the two legs meet. This is due to the discrete nature of Minecraft blocks approximating the continuous catenary curve. For best results, manually smooth out any irregular blocks at the peak after placing the schematic. This typically only affects a small area (10-20 blocks) at the apex.

## Performance Notes

- **Memory**: Large arches (scale > 1.0) require several GB of RAM
- **Generation Time**: Proportional to scale³ (doubling scale = 8x time)
- **File Size**: Hollow arches are ~70% smaller than solid
- **Hollow Recommended**: Use hollow for scale > 0.5

## Troubleshooting

### Import Error

```
ModuleNotFoundError: No module named 'litematica'
```

**Solution**: The litematica library must be in the parent directory. Ensure you're running from the correct location:

```bash
cd TheresTheArch
python theresthearch/arch_gui.py
```

### Out of Memory

If generation fails with memory error:
1. Reduce scale
2. Use hollow construction
3. Close other applications
4. Increase system swap space

### Generation Too Slow

For faster generation:
1. Use smaller scale
2. Reduce wall thickness (hollow)
3. Use solid SSD for output
4. Close background applications

## Credits

- **Gateway Arch**: Designed by Eero Saarinen, completed 1965
- **Mathematical Equation**: [Wikipedia - Gateway Arch](https://en.wikipedia.org/wiki/Gateway_Arch)
- **Litematica Format**: [Litematica Mod](https://github.com/maruohon/litematica)

## See Also

- [Litematica Python Library](../litematica-python/) - The underlying schematic library
- [Gateway Arch Wikipedia](https://en.wikipedia.org/wiki/Gateway_Arch) - Historical and mathematical information
- [Gateway Arch Official Site](https://www.gatewayarch.com/) - Visit the real arch!

## License

See LICENSE file for details.

---

**Built with ❤️ using the actual Gateway Arch mathematics**


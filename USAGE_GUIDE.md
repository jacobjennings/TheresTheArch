# TheresTheArch - Complete Usage Guide

This guide covers everything you need to know about generating Gateway Arch schematics.

## Table of Contents

1. [Quick Start](#quick-start)
2. [GUI Application](#gui-application)
3. [Command Line Usage](#command-line-usage)
4. [Python API](#python-api)
5. [Mathematical Background](#mathematical-background)
6. [Customization Guide](#customization-guide)
7. [Performance Tips](#performance-tips)
8. [Troubleshooting](#troubleshooting)

## Quick Start

### Installation

```bash
cd TheresTheArch
pip install -r theresthearch/requirements.txt
pip install -r litematica-python/requirements.txt
```

### Generate Your First Arch

**Option 1: GUI (Easiest)**

```bash
python theresthearch/arch_gui.py
```

**Option 2: Command Line**

```python
python -c "from theresthearch import create_simple_arch; create_simple_arch(scale=0.3, output_file='my_arch.litematic')"
```

## GUI Application

### Launching

```bash
cd TheresTheArch
python theresthearch/arch_gui.py
```

Or use the launcher script:

```bash
./theresthearch/run_gui.sh
```

### GUI Features

#### Scale Options

**Scale Slider (0.1 - 2.0)**
- Adjusts the overall size of the arch
- 1.0 = Full size (630 blocks tall)
- 0.5 = Half size (315 blocks tall)
- Real-time height display

**Scale Guide:**
- **0.1-0.25**: Small test builds (63-158 blocks)
- **0.3-0.5**: Standard servers (189-315 blocks)
- **0.6-1.0**: Large builds (378-630 blocks)
- **1.0-2.0**: Epic projects (630-1260 blocks)

#### Structure Options

**Hollow Interior**
- ✅ Checked: Creates hollow arch (recommended for large builds)
- ❌ Unchecked: Creates solid arch (better for small builds)

**Wall Thickness (1-10 blocks)**
- Only applies when hollow
- Recommended: 3-5 blocks for most scales
- Thicker walls = more blocks but sturdier appearance

#### Block Types

**Primary Block**
- Main block used for the arch structure
- Choose from 15+ common building blocks
- Examples: Quartz, Concrete, Stone Bricks

**Corner/Edge Block**
- Block used for edges and corners
- Leave empty to use same as primary
- Adds visual detail and structural definition

**Popular Combinations:**
1. Quartz Block + Quartz Pillar
2. White Concrete + Light Gray Concrete
3. Stone Bricks + Chiseled Stone Bricks
4. Iron Block + Dark Oak Log

#### Preview Panel

**Dimensions Display:**
- **Overall**: Total schematic size (W × H × D)
- **Base**: Dimensions at ground level
- **Peak**: Dimensions at the top

**Block Counts:**
- Estimated count per block type
- Total blocks required
- Updates automatically when options change

#### Output Options

**Output File**
- Specify where to save the .litematic file
- Use "Browse" button for file dialog
- Default: `gateway_arch.litematic`

### Generating

1. Configure all options
2. Review preview information
3. Click "Generate Schematic"
4. Wait for progress bar to complete
5. Success message shows output location

## Command Line Usage

### Simple Generation

```python
from theresthearch import create_simple_arch

# Basic usage
create_simple_arch(scale=0.5, output_file="arch.litematic")
```

This creates a hollow arch with default settings:
- Primary block: Quartz
- Corner block: Quartz Pillar
- Thickness: 3 blocks

### Custom Parameters

```python
from theresthearch import ArchGenerator

generator = ArchGenerator(
    scale=0.75,
    hollow=True,
    thickness=5,
    primary_block="minecraft:white_concrete",
    corner_block="minecraft:light_gray_concrete"
)

# Get information before generating
dims = generator.calculate_dimensions()
print(f"Will be {dims['overall'][1]} blocks tall")

blocks = generator.estimate_blocks()
total = sum(blocks.values())
print(f"Estimated {total:,} total blocks")

# Generate
schematic = generator.generate()
schematic.save("custom_arch.litematic")
```

## Python API

### ArchGenerator Class

#### Constructor

```python
generator = ArchGenerator(
    scale: float = 1.0,          # Size multiplier
    hollow: bool = False,        # Hollow interior?
    thickness: int = 3,          # Wall thickness (if hollow)
    primary_block: str = "...",  # Main block type
    corner_block: str = None     # Corner block (None = same as primary)
)
```

#### Methods

**`calculate_dimensions() -> Dict`**

Returns dimensions dictionary:

```python
dims = generator.calculate_dimensions()
# Returns: {
#   'base': (width, height, depth),
#   'peak': (width, height, depth),
#   'overall': (width, height, depth)
# }
```

**`estimate_blocks() -> Dict[str, int]`**

Returns estimated block counts:

```python
blocks = generator.estimate_blocks()
# Returns: {
#   'minecraft:quartz_block': 150000,
#   'minecraft:quartz_pillar': 50000
# }
```

**`generate(progress_callback=None) -> LitematicaSchematic`**

Generates the schematic:

```python
def my_progress(current, total, message):
    print(f"{message}: {current}/{total}")

schematic = generator.generate(progress_callback=my_progress)
schematic.save("output.litematic")
```

### Helper Functions

**`create_simple_arch(scale, output_file)`**

Quick arch generation:

```python
from theresthearch import create_simple_arch

create_simple_arch(
    scale=0.4,
    output_file="quick_arch.litematic"
)
```

## Mathematical Background

### The Catenary Equation

The Gateway Arch follows a **weighted catenary curve**, defined by:

```
y = A - B × cosh(C × x)
```

Where:
- **A** = 693.8597 feet (vertical shift)
- **B** = 68.7672 feet (amplitude)
- **C** = 0.0100333 (horizontal scaling)
- **cosh** = hyperbolic cosine function

### Implementation

The generator:

1. **Samples points** around the arch perimeter
2. **Calculates height** using the catenary equation
3. **Fills between** inner and outer radii (if hollow)
4. **Identifies corners** based on neighbor count
5. **Places blocks** with appropriate types

### Coordinate System

- **X-axis**: West to East
- **Y-axis**: Ground to Sky (height)
- **Z-axis**: North to South
- **Origin**: Center of arch at ground level

## Customization Guide

### Choosing Block Types

#### For Modern Builds
```python
primary_block="minecraft:white_concrete"
corner_block="minecraft:light_gray_concrete"
```

#### For Medieval/Fantasy
```python
primary_block="minecraft:stone_bricks"
corner_block="minecraft:chiseled_stone_bricks"
```

#### For Futuristic/Tech
```python
primary_block="minecraft:iron_block"
corner_block="minecraft:observer"
```

#### For Natural/Organic
```python
primary_block="minecraft:moss_block"
corner_block="minecraft:oak_log"
```

### Scale Selection Guide

| Use Case | Recommended Scale | Height | Block Count |
|----------|------------------|--------|-------------|
| Testing | 0.1 - 0.2 | 63-126 | 10k-50k |
| Small Server | 0.3 - 0.4 | 189-252 | 100k-200k |
| Standard Build | 0.5 - 0.6 | 315-378 | 300k-500k |
| Large Project | 0.7 - 0.9 | 441-567 | 700k-1.5M |
| Full Scale | 1.0 | 630 | 2M+ |
| Epic Build | 1.5 - 2.0 | 945-1260 | 5M-10M+ |

### Hollow vs Solid

**Hollow (Recommended for scale > 0.4)**
- ✅ Uses 60-80% fewer blocks
- ✅ Faster to load in game
- ✅ Better performance
- ✅ Interior space usable
- ❌ More complex generation
- ❌ Requires thickness setting

**Solid (Good for scale < 0.4)**
- ✅ Simpler structure
- ✅ Faster generation
- ✅ More solid appearance
- ❌ Uses many more blocks
- ❌ Heavier to render
- ❌ No interior space

### Thickness Guidelines

| Scale | Recommended Thickness |
|-------|--------------------|
| 0.1-0.3 | 1-2 blocks |
| 0.4-0.6 | 3-4 blocks |
| 0.7-1.0 | 5-7 blocks |
| 1.1-2.0 | 8-10 blocks |

## Performance Tips

### Generation Speed

**Faster:**
- Use smaller scales
- Use solid construction (simpler algorithm)
- Close other applications
- Use SSD for output

**Slower:**
- Large scales (>1.0)
- Hollow with small thickness
- HDD storage
- Low RAM

### Memory, file size, and time

Generation cost scales roughly with the block count (volume), so doubling the
scale increases memory, file size, and time by roughly 8×. Concrete numbers
depend heavily on your machine, the scale, and whether the build is hollow.

Rather than relying on fixed estimates:

- **Check the live preview** (CLI/GUI) for the exact block count before
  generating — that's the best predictor of cost.
- **Prefer hollow construction** for large scales; it dramatically reduces block
  count, memory, and file size versus solid.
- **To reduce memory:** lower the scale, use hollow construction, and close
  other applications.

## Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'litematica'"

**Cause**: Litematica library not found

**Solution**:
```bash
cd TheresTheArch
# Make sure you're in the project root
python theresthearch/arch_gui.py
```

#### "ModuleNotFoundError: No module named 'nbt'"

**Cause**: NBT library not installed

**Solution**:
```bash
pip install NBT
```

#### "MemoryError" or "Out of Memory"

**Cause**: Not enough RAM for the selected scale

**Solutions**:
1. Reduce scale
2. Use hollow construction
3. Close other applications
4. Increase system swap/page file

#### Generation is Too Slow

**Solutions**:
1. Reduce scale
2. Use solid instead of hollow
3. Reduce wall thickness
4. Close background applications
5. Use faster CPU

#### File Won't Load in Minecraft

**Possible Causes**:
1. File too large for available RAM
2. Litematica mod not installed
3. Wrong Minecraft version

**Solutions**:
1. Reduce scale and regenerate
2. Install Litematica mod
3. Check mod compatibility

### GUI Issues

#### Window Doesn't Open

**Solution**:
```bash
# Check if tkinter is installed
python3 -m tkinter
# Should open a test window

# If not installed:
# Ubuntu/Debian:
sudo apt-get install python3-tk
# Fedora:
sudo dnf install python3-tkinter
# macOS: (included with Python)
# Windows: Reinstall Python with tcl/tk option
```

#### Preview Not Updating

**Solution**:
1. Click "Update Preview" button
2. Change a value to trigger update
3. Restart application

## Advanced Usage

### Batch Generation

Generate multiple scales:

```python
from theresthearch import ArchGenerator

scales = [0.3, 0.5, 0.7, 1.0]

for scale in scales:
    print(f"\nGenerating scale {scale}...")
    generator = ArchGenerator(scale=scale, hollow=True)
    schematic = generator.generate()
    schematic.save(f"arch_scale_{scale}.litematic")
    print(f"Saved arch_scale_{scale}.litematic")
```

### Custom Block Selection

Create themed arches:

```python
themes = {
    'quartz': ('minecraft:quartz_block', 'minecraft:quartz_pillar'),
    'modern': ('minecraft:white_concrete', 'minecraft:light_gray_concrete'),
    'stone': ('minecraft:stone_bricks', 'minecraft:chiseled_stone_bricks'),
    'metal': ('minecraft:iron_block', 'minecraft:dark_oak_log'),
}

for theme_name, (primary, corner) in themes.items():
    generator = ArchGenerator(
        scale=0.4,
        hollow=True,
        primary_block=primary,
        corner_block=corner
    )
    schematic = generator.generate()
    schematic.save(f"arch_{theme_name}.litematic")
```

### Progress Monitoring

Detailed progress tracking:

```python
import time

def detailed_progress(current, total, message):
    percent = (current / total) * 100
    bar_length = 40
    filled = int(bar_length * current / total)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f'\r{message}: |{bar}| {percent:.1f}%', end='', flush=True)

generator = ArchGenerator(scale=0.5)
start = time.time()
schematic = generator.generate(progress_callback=detailed_progress)
elapsed = time.time() - start
print(f"\n\nGeneration completed in {elapsed:.1f} seconds")
```

## Examples

See the examples in [theresthearch/README.md](theresthearch/README.md) for more code samples.

## Support

For issues, questions, or contributions:
1. Check this guide first
2. Review the README files
3. Check existing GitHub issues
4. Open a new issue with details

## See Also

- [Main README](README.md) - Project overview
- [Litematica Library](litematica-python/README.md) - Underlying library
- [Gateway Arch Wikipedia](https://en.wikipedia.org/wiki/Gateway_Arch) - Real arch information
- [Litematica Mod](https://github.com/maruohon/litematica) - Minecraft mod

---

Happy building! 🏗️🌉


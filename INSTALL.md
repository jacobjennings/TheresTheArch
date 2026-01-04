# Installation Guide

Complete installation instructions for TheresTheArch project.

## Quick Start (Recommended)

Run the automated setup script:

```bash
cd TheresTheArch
./setup.sh
```

This will:
1. Create a Python virtual environment
2. Install the NBT library
3. Check for tkinter (GUI support)
4. Display usage instructions

Then activate the virtual environment:

```bash
source venv/bin/activate
```

## Manual Installation

### Step 1: Prerequisites

- **Python 3.7+** (check with `python3 --version`)
- **pip** (usually included with Python)

### Step 2: Create Virtual Environment

Modern Linux distributions require using a virtual environment:

```bash
cd TheresTheArch

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

**Note:** If you get an error about `venv` not being available:

```bash
# Ubuntu/Debian
sudo apt-get install python3-venv

# Fedora/RHEL
sudo dnf install python3-virtualenv
```

### Step 3: Install Dependencies

With the virtual environment activated:

```bash
pip install NBT
```

This installs the NBT library required for reading/writing Litematica files.

### Step 4: Install tkinter (Optional, for GUI)

The GUI requires tkinter. Check if you have it:

```bash
python3 -c "import tkinter"
```

If you get an error, install tkinter:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S tk
```

**macOS:**
Tkinter is included with Python on macOS.

**Windows:**
Tkinter is included with Python on Windows.

**Note:** You can use the command-line interface even without tkinter!

## Usage After Installation

### Always Activate Virtual Environment First

Before using the project:

```bash
cd TheresTheArch
source venv/bin/activate
```

### Run the Application

**Command-line interface (no tkinter needed):**
```bash
python theresthearch/arch_cli.py
```

**GUI (requires tkinter):**
```bash
python theresthearch/arch_gui.py
```

**Python API:**
```python
from theresthearch import create_simple_arch
create_simple_arch(scale=0.5, output_file="arch.litematic")
```

### Deactivate Virtual Environment

When done:

```bash
deactivate
```

## Troubleshooting

### "No module named 'nbt'"

**Problem:** NBT library not installed or virtual environment not activated.

**Solution:**
```bash
cd TheresTheArch
source venv/bin/activate
pip install NBT
```

### "No module named 'tkinter'"

**Problem:** tkinter not installed (only affects GUI).

**Solution 1:** Install tkinter (see Step 4 above)

**Solution 2:** Use the command-line interface instead:
```bash
python theresthearch/arch_cli.py
```

### "externally-managed-environment" Error

**Problem:** Trying to install packages system-wide on modern Linux.

**Solution:** Use a virtual environment (see Step 2 above).

### "command not found: python3"

**Problem:** Python 3 not installed.

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3

# Fedora/RHEL
sudo dnf install python3

# Arch Linux
sudo pacman -S python
```

### Virtual Environment Not Activating

**Problem:** Shell doesn't support `source` command.

**Solutions:**

For bash/zsh:
```bash
source venv/bin/activate
```

For fish:
```bash
source venv/bin/activate.fish
```

For csh/tcsh:
```bash
source venv/bin/activate.csh
```

For PowerShell (Windows):
```powershell
venv\Scripts\Activate.ps1
```

### Permission Denied on setup.sh

**Problem:** Script not executable.

**Solution:**
```bash
chmod +x setup.sh
./setup.sh
```

## Platform-Specific Notes

### Ubuntu/Debian

Full installation:
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv python3-tk
cd TheresTheArch
./setup.sh
```

### Fedora/RHEL

Full installation:
```bash
sudo dnf install python3 python3-pip python3-tkinter
cd TheresTheArch
./setup.sh
```

### Arch Linux

Full installation:
```bash
sudo pacman -S python python-pip tk
cd TheresTheArch
./setup.sh
```

### macOS

Python and tkinter are usually pre-installed. Just run:
```bash
cd TheresTheArch
./setup.sh
```

If you need Python 3:
```bash
brew install python3
```

### Windows

1. Install Python 3 from [python.org](https://www.python.org/)
2. Make sure to check "Add Python to PATH" during installation
3. Open PowerShell or Command Prompt:
```powershell
cd TheresTheArch
python -m venv venv
venv\Scripts\activate
pip install NBT
python theresthearch\arch_cli.py
```

## Verifying Installation

Test that everything works:

```bash
# Activate virtual environment
source venv/bin/activate

# Test NBT library
python -c "from nbt import nbt; print('NBT: OK')"

# Test litematica library
python -c "from litematica import LitematicaSchematic; print('Litematica: OK')"

# Test arch generator
python -c "from theresthearch import ArchGenerator; print('ArchGenerator: OK')"

# Test tkinter (optional)
python -c "import tkinter; print('tkinter: OK')"
```

If all tests pass, you're ready to generate Gateway Arch schematics!

## Next Steps

After installation:

1. **Quick Test**: Run the CLI and select preset #1 (small test arch)
   ```bash
   python theresthearch/arch_cli.py
   ```

2. **Read Documentation**: Check out the usage guides
   - [USAGE_GUIDE.md](USAGE_GUIDE.md)
   - [theresthearch/README.md](theresthearch/README.md)

3. **Generate Your Arch**: Use the interactive CLI or GUI to create your custom arch

## Getting Help

If you encounter issues:

1. Check this guide
2. Review error messages carefully
3. Make sure virtual environment is activated
4. Check that all dependencies are installed
5. Try the command-line interface if GUI fails
6. Open an issue on GitHub with error details

## Uninstallation

To remove the project:

```bash
cd TheresTheArch
deactivate  # if virtual environment is active
rm -rf venv  # remove virtual environment
cd ..
rm -rf TheresTheArch  # remove project folder
```

---

**Need more help?** See [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed usage instructions.


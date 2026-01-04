#!/bin/bash
# Setup script for TheresTheArch project

echo "=================================="
echo "TheresTheArch Setup"
echo "=================================="
echo

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python version: $(python3 --version)"
echo

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        echo "You may need to install python3-venv:"
        echo "  sudo apt-get install python3-venv"
        exit 1
    fi
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo
echo "Installing dependencies..."
pip install --upgrade pip

echo
echo "Installing NBT library..."
pip install NBT

if [ $? -eq 0 ]; then
    echo "✓ NBT library installed"
else
    echo "Error: Failed to install NBT library"
    exit 1
fi

# Check for tkinter
echo
echo "Checking for tkinter..."
if python3 -c "import tkinter" 2>/dev/null; then
    echo "✓ tkinter is available (GUI will work)"
    GUI_AVAILABLE=true
else
    echo "⚠ tkinter is not available (GUI will not work)"
    echo "  To install tkinter:"
    echo "    Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "    Fedora:        sudo dnf install python3-tkinter"
    echo "    Arch:          sudo pacman -S tk"
    echo
    echo "  You can still use the command-line interface!"
    GUI_AVAILABLE=false
fi

echo
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo
echo "To use TheresTheArch:"
echo
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo
echo "2. Run the command-line interface:"
echo "   python theresthearch/arch_cli.py"
echo

if [ "$GUI_AVAILABLE" = true ]; then
    echo "3. Or run the GUI:"
    echo "   python theresthearch/arch_gui.py"
    echo
fi

echo "To deactivate the virtual environment:"
echo "   deactivate"
echo


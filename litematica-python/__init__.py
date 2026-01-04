"""
Litematica Python Library

A Python library for reading, writing, and manipulating Litematica schematic files.
"""

from .litematica import (
    LitematicaSchematic,
    Region,
    BlockState,
    SchematicMetadata,
    BitArray,
)

__version__ = "1.0.0"
__author__ = "TheresTheArch"
__all__ = [
    "LitematicaSchematic",
    "Region",
    "BlockState",
    "SchematicMetadata",
    "BitArray",
]


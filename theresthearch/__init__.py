"""
TheresTheArch - Gateway Arch Schematic Generator

Generate Minecraft schematics of the Gateway Arch using the mathematical
catenary equation from the actual Gateway Arch in St. Louis.
"""

from .arch_generator import ArchGenerator, create_simple_arch

__version__ = "1.0.0"
__author__ = "TheresTheArch"
__all__ = ["ArchGenerator", "create_simple_arch"]


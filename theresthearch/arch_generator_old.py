"""
Gateway Arch Schematic Generator

Generates Minecraft schematics of the Gateway Arch using the mathematical
catenary equation from the actual Gateway Arch in St. Louis.

Based on: https://en.wikipedia.org/wiki/Gateway_Arch
Equation: y = 693.8597 - 68.7672 * cosh(0.0100333 * x)
"""

import math
import sys
import os
from typing import Dict, Set, Tuple, Optional
from collections import Counter

# Add parent directory to path to import litematica library
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'litematica-python'))

from litematica import LitematicaSchematic, Region, BlockState


class ArchGenerator:
    """Generates Gateway Arch schematics using the catenary equation."""
    
    # Original Gateway Arch parameters (in feet)
    ORIGINAL_HEIGHT = 630  # feet
    ORIGINAL_WIDTH = 630   # feet
    
    # Catenary equation coefficients
    A = 693.8597
    B = 68.7672
    C = 0.0100333
    
    def __init__(self, scale: float = 1.0, girth_scale: float = 1.0, hollow: bool = False, 
                 thickness: int = 1, primary_block: str = "minecraft:iron_block",
                 corner_block: Optional[str] = None):
        """
        Initialize arch generator.
        
        Args:
            scale: Scale factor for height (1.0 = 630 blocks tall)
            girth_scale: Scale factor for width (1.0 = 630 blocks wide)
            hollow: Whether the arch should be hollow
            thickness: Thickness of arch walls (if hollow)
            primary_block: Block ID for main structure
            corner_block: Block ID for corners/edges (None = use primary)
        """
        self.scale = scale
        self.girth_scale = girth_scale
        self.hollow = hollow
        self.thickness = max(1, thickness)
        self.primary_block = primary_block
        self.corner_block = corner_block or primary_block
        
        # Calculate scaled dimensions
        self.height = int(self.ORIGINAL_HEIGHT * scale)
        self.width = int(self.ORIGINAL_WIDTH * girth_scale)
        
    def catenary(self, x: float) -> float:
        """
        Calculate y-coordinate for given x using Gateway Arch catenary equation.
        
        The equation is: y = A - B * cosh(C * x)
        Where A = 693.8597, B = 68.7672, C = 0.0100333
        
        Args:
            x: X-coordinate in original arch scale
            
        Returns:
            Y-coordinate in original arch scale
        """
        return self.A - self.B * math.cosh(self.C * x)
    
    def get_arch_y(self, x: int, z: int) -> Optional[int]:
        """
        Get the y-coordinate (height) for a given (x, z) position in the arch.
        
        Args:
            x: X-coordinate in blocks (centered at width/2)
            z: Z-coordinate in blocks (centered at width/2)
            
        Returns:
            Y-coordinate in blocks, or None if outside arch
        """
        # Calculate distance from center axis
        center = self.width / 2
        dx = x - center
        dz = z - center
        distance = math.sqrt(dx * dx + dz * dz)
        
        # Convert to original scale (use girth_scale for width)
        x_original = (distance / self.girth_scale) - (self.ORIGINAL_WIDTH / 2)
        
        # Check if within arch bounds
        if abs(x_original) > self.ORIGINAL_WIDTH / 2:
            return None
        
        # Calculate height using catenary
        y_original = self.catenary(x_original)
        
        # Ground level is at y = 625 in original (arch is 625 feet above ground to 1255)
        # We want ground at y = 0, so subtract minimum height
        y_min = self.catenary(self.ORIGINAL_WIDTH / 2)  # Height at edges
        y_adjusted = y_original - y_min
        
        # Scale to blocks
        y_blocks = int(y_adjusted * self.scale)
        
        return max(0, y_blocks)
    
    def should_place_block(self, x: int, y: int, z: int, 
                          inner_radius: float, outer_radius: float) -> bool:
        """
        Determine if a block should be placed at the given position.
        
        Args:
            x, y, z: Block coordinates
            inner_radius: Inner radius at this height (for hollow arch)
            outer_radius: Outer radius at this height
            
        Returns:
            True if block should be placed
        """
        center = self.width / 2
        dx = x - center
        dz = z - center
        distance = math.sqrt(dx * dx + dz * dz)
        
        # Check if within outer radius
        if distance > outer_radius:
            return False
        
        # If solid, place all blocks within outer radius
        if not self.hollow:
            return True
        
        # If hollow, only place blocks between inner and outer radius
        return distance >= inner_radius
    
    def is_corner_block(self, x: int, y: int, z: int, 
                       neighbor_count: int) -> bool:
        """
        Determine if a block is on a corner/edge.
        
        Args:
            x, y, z: Block coordinates
            neighbor_count: Number of neighboring blocks
            
        Returns:
            True if this is a corner/edge block
        """
        # Blocks with fewer neighbors are on edges/corners
        return neighbor_count < 6
    
    def calculate_dimensions(self) -> Dict[str, Tuple[int, int, int]]:
        """
        Calculate arch dimensions.
        
        Returns:
            Dictionary with 'base', 'peak', and 'overall' dimensions
        """
        # Base is approximately the width at ground level
        base_width = self.width
        base_depth = self.width
        base_height = self.thickness * 2  # Approximate base height
        
        # Peak is the top of the arch
        peak_width = self.thickness * 2
        peak_depth = self.thickness * 2
        peak_height = self.thickness
        
        # Overall dimensions
        overall_width = self.width
        overall_height = self.height
        overall_depth = self.width
        
        return {
            'base': (base_width, base_height, base_depth),
            'peak': (peak_width, peak_height, peak_depth),
            'overall': (overall_width, overall_height, overall_depth)
        }
    
    def estimate_blocks(self) -> Dict[str, int]:
        """
        Estimate block counts without generating full structure.
        
        Returns:
            Dictionary with block type counts
        """
        block_counts = Counter()
        
        # Sample every few blocks for estimation
        sample_rate = max(1, int(self.scale * 5))
        
        for x in range(0, self.width, sample_rate):
            for z in range(0, self.width, sample_rate):
                max_y = self.get_arch_y(x, z)
                if max_y is None:
                    continue
                
                for y in range(max_y):
                    # Calculate radii at this height
                    height_ratio = y / max(1, self.height)
                    base_radius = self.width / 2
                    top_radius = self.thickness
                    outer_radius = base_radius - (base_radius - top_radius) * height_ratio
                    inner_radius = outer_radius - self.thickness if self.hollow else 0
                    
                    if self.should_place_block(x, y, z, inner_radius, outer_radius):
                        # Simplified corner detection for estimate
                        center = self.width / 2
                        dx = x - center
                        dz = z - center
                        distance = math.sqrt(dx * dx + dz * dz)
                        
                        if abs(distance - outer_radius) < 2 or abs(distance - inner_radius) < 2:
                            block_counts[self.corner_block] += 1
                        else:
                            block_counts[self.primary_block] += 1
        
        # Scale up estimate based on sample rate
        scale_factor = sample_rate ** 2
        return {block: count * scale_factor for block, count in block_counts.items()}
    
    def generate(self, progress_callback=None) -> LitematicaSchematic:
        """
        Generate the Gateway Arch schematic.
        
        Args:
            progress_callback: Optional callback function(current, total, message)
            
        Returns:
            LitematicaSchematic object
        """
        # Create schematic
        schematic = LitematicaSchematic()
        schematic.metadata.name = f"Gateway Arch (Scale {self.scale:.2f})"
        schematic.metadata.author = "TheresTheArch Generator"
        schematic.metadata.description = (
            f"Gateway Arch generated using catenary equation. "
            f"Scale: {self.scale:.2f}, "
            f"{'Hollow' if self.hollow else 'Solid'}, "
            f"Blocks: {self.primary_block}"
        )
        
        # Create region
        region = Region(
            "Arch",
            position=(0, 0, 0),
            size=(self.width, self.height, self.width)
        )
        
        # Pre-create block states
        primary_state = BlockState(self.primary_block)
        corner_state = BlockState(self.corner_block)
        
        # Track blocks for neighbor analysis
        blocks_to_place: Dict[Tuple[int, int, int], bool] = {}
        
        # First pass: determine which blocks to place
        total_positions = self.width * self.width
        current = 0
        
        if progress_callback:
            progress_callback(0, total_positions, "Calculating arch shape...")
        
        for x in range(self.width):
            for z in range(self.width):
                current += 1
                if progress_callback and current % 100 == 0:
                    progress_callback(current, total_positions, "Calculating arch shape...")
                
                max_y = self.get_arch_y(x, z)
                if max_y is None:
                    continue
                
                for y in range(max_y):
                    # Calculate radii at this height
                    height_ratio = y / max(1, self.height)
                    base_radius = self.width / 2
                    top_radius = self.thickness
                    outer_radius = base_radius - (base_radius - top_radius) * height_ratio
                    inner_radius = outer_radius - self.thickness if self.hollow else 0
                    
                    if self.should_place_block(x, y, z, inner_radius, outer_radius):
                        blocks_to_place[(x, y, z)] = False  # False = not yet identified as corner
        
        # Second pass: identify corners and place blocks
        total_blocks = len(blocks_to_place)
        current = 0
        
        if progress_callback:
            progress_callback(0, total_blocks, "Placing blocks...")
        
        for (x, y, z) in blocks_to_place:
            current += 1
            if progress_callback and current % 1000 == 0:
                progress_callback(current, total_blocks, "Placing blocks...")
            
            # Count neighbors
            neighbor_count = 0
            for dx, dy, dz in [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)]:
                if (x+dx, y+dy, z+dz) in blocks_to_place:
                    neighbor_count += 1
            
            # Place appropriate block
            if self.is_corner_block(x, y, z, neighbor_count):
                region.set_block(x, y, z, corner_state)
            else:
                region.set_block(x, y, z, primary_state)
        
        # Add region to schematic
        schematic.add_region(region)
        
        if progress_callback:
            progress_callback(total_blocks, total_blocks, "Complete!")
        
        return schematic


def create_simple_arch(scale: float = 0.5, girth_scale: float = None, output_file: str = "gateway_arch.litematic"):
    """
    Create a simple Gateway Arch schematic (convenience function).
    
    Args:
        scale: Scale factor for height (0.5 = 315 blocks tall)
        girth_scale: Scale factor for width (None = same as scale)
        output_file: Output filename
    """
    if girth_scale is None:
        girth_scale = scale
    
    print(f"Generating Gateway Arch at scale {scale} (girth {girth_scale})...")
    
    generator = ArchGenerator(
        scale=scale,
        girth_scale=girth_scale,
        hollow=True,
        thickness=1,
        primary_block="minecraft:iron_block",
        corner_block=None
    )
    
    # Show dimensions
    dims = generator.calculate_dimensions()
    print(f"\nDimensions:")
    print(f"  Overall: {dims['overall'][0]}W × {dims['overall'][1]}H × {dims['overall'][2]}D blocks")
    print(f"  Base: {dims['base'][0]}W × {dims['base'][1]}H × {dims['base'][2]}D blocks")
    print(f"  Peak: {dims['peak'][0]}W × {dims['peak'][1]}H × {dims['peak'][2]}D blocks")
    
    # Estimate blocks
    print(f"\nEstimating blocks...")
    blocks = generator.estimate_blocks()
    for block_type, count in blocks.items():
        stacks = count / 64
        shulkers = count / (27 * 64)
        print(f"  {block_type}:")
        print(f"    ~{count:,} blocks")
        print(f"    ~{stacks:.1f} stacks")
        print(f"    ~{shulkers:.2f} shulker boxes")
    
    # Generate
    print(f"\nGenerating schematic...")
    
    def progress(current, total, message):
        percent = (current / total) * 100
        print(f"\r{message} {percent:.1f}%", end='', flush=True)
    
    schematic = generator.generate(progress_callback=progress)
    print()  # New line after progress
    
    # Save
    print(f"Saving to {output_file}...")
    schematic.save(output_file)
    print(f"Done! Schematic saved to {output_file}")


if __name__ == "__main__":
    create_simple_arch(scale=0.3, output_file="gateway_arch_small.litematic")


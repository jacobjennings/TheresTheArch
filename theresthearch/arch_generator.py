"""
Gateway Arch Schematic Generator - Accurate Version

Generates Minecraft schematics of the Gateway Arch with accurate leg geometry.
The real arch has two triangular-cross-section legs, not a circular design.

Mathematical basis:
- Gateway Arch uses a "weighted catenary" (flattened catenary) curve
- Equation: y = A - B * cosh(C * x) where A=693.8597, B=68.7672, C=0.0100333
- Reference: "Mathematics of the Gateway Arch" by Robert Osserman (AMS Notices)
- The arch's D value (A*B*C) ≈ 0.69, making it a flattened catenary
- Cross-section is an equilateral triangle tapering from 54ft at base to 17ft at top

Based on: https://en.wikipedia.org/wiki/Gateway_Arch
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
    """Generates Gateway Arch schematics with accurate triangular leg geometry."""
    
    # Original Gateway Arch parameters (in feet)
    ORIGINAL_HEIGHT = 630  # feet
    ORIGINAL_WIDTH = 630   # feet (between leg centers)
    
    # Leg dimensions (in feet)
    LEG_BASE_WIDTH = 54    # Width of each leg face at base
    LEG_TOP_WIDTH = 17     # Width of each leg face at top
    
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
        self.design_height = int(self.ORIGINAL_HEIGHT * scale)
        self.design_width = int(self.ORIGINAL_WIDTH * girth_scale)
        
        # Calculate leg widths at base and top (scaled)
        self.leg_base_width = int(self.LEG_BASE_WIDTH * girth_scale)
        self.leg_top_width = int(self.LEG_TOP_WIDTH * girth_scale)

        # Add padding to accommodate leg thickness extending beyond the centerline span
        # Leg extends outwards by approx 2/3 height of triangle ~ 35 feet.
        # 35 feet * girth_scale = padding in blocks.
        # Safe padding: leg_base_width (blocks) should be enough.
        self.padding = self.leg_base_width + 5
        
        # Actual schematic dimensions
        # Width needs padding on both sides
        self.width = self.design_width + 2 * self.padding
        # Height needs padding at the top for the flat face of the triangle
        self.height = self.design_height + self.padding
        
        # Precompute catenary bounds to map block grid to full arch shape
        # y_peak is height at center (x=0)
        self.y_peak = self.catenary(0)
        # y_min is height at base (x=width/2)
        self.y_min = self.catenary(self.ORIGINAL_WIDTH / 2)
        self.y_range = self.y_peak - self.y_min
        
    def catenary(self, x: float) -> float:
        """Calculate y-coordinate using Gateway Arch catenary equation."""
        return self.A - self.B * math.cosh(self.C * x)
    
    def catenary_prime(self, x: float) -> float:
        """Calculate derivative dy/dx."""
        return -self.B * self.C * math.sinh(self.C * x)

    def get_leg_width_at_height(self, y: int) -> int:
        """Get the width of the leg at a given height (Y block coord)."""
        if y >= self.height:
            return self.leg_top_width
        
        # Linear taper from base to top
        ratio = y / self.height
        width = self.leg_base_width - (self.leg_base_width - self.leg_top_width) * ratio
        return max(int(width), self.leg_top_width)

    def get_leg_width_at_feet_y(self, y_feet: float) -> float:
        """
        Get leg width in feet at a specific Y height (in feet).
        
        IMPORTANT: Returns QUANTIZED width to prevent sawtooth aliasing.
        The width is snapped to integer block units, ensuring clean transitions
        as the arch tapers. Without quantization, continuous float widths cause
        irregular stepping when rasterized to blocks.
        """
        if y_feet >= self.A:  # Top of arch formula max
            return self.LEG_TOP_WIDTH
             
        # Map Y feet to ratio [0, 1]
        ratio = (y_feet - self.y_min) / self.y_range
        ratio = max(0.0, min(1.0, ratio))
        
        # Calculate continuous width first
        continuous_width = self.LEG_BASE_WIDTH - (self.LEG_BASE_WIDTH - self.LEG_TOP_WIDTH) * ratio
        
        # QUANTIZE: Convert to block units, floor to integer, convert back to feet
        # This ensures the triangle size only changes at clean block boundaries
        # 1 block = 1/girth_scale feet
        feet_per_block = 1.0 / self.girth_scale
        
        # Convert width from feet to blocks, quantize, convert back
        width_in_blocks = continuous_width * self.girth_scale
        quantized_blocks = math.floor(width_in_blocks)
        
        # Ensure we don't go below minimum
        quantized_blocks = max(quantized_blocks, self.leg_top_width)
        
        # Convert back to feet
        return quantized_blocks * feet_per_block

    def get_closest_curve_point(self, x_feet: float, y_feet: float) -> Tuple[float, float]:
        """
        Find the point (xc, yc) on the catenary curve that is closest to (x, y).
        This is essential for determining the 'normal' plane for the cross section.
        Uses simple Newton-Raphson or approximation.
        Since the arch is thin, xc ≈ x_feet is a very good start.
        """
        # Initial guess
        xc = x_feet
        
        # 2 iterations of Newton's method to find xc where normal passes through (x,y)
        # Minimize distance squared D^2 = (x-xc)^2 + (y - f(xc))^2
        # Or simpler: The normal at xc must pass through (x,y).
        # Normal slope is -1/f'(xc).
        # Slope from (xc, yc) to (x, y) is (y-yc)/(x-xc).
        # (y-yc)/(x-xc) = -1/f'(xc) => (y-yc)*f'(xc) + (x-xc) = 0.
        # F(xc) = (y - f(xc))*f'(xc) + x - xc = 0
        
        for _ in range(3):
            # Clamp xc to prevent overflow/instability
            if abs(xc) > self.ORIGINAL_WIDTH * 2:
                xc = x_feet # Reset if exploded
                break

            try:
                yc = self.catenary(xc)
                dy = self.catenary_prime(xc)
                ddy = -self.B * (self.C**2) * math.cosh(self.C * xc) # f''(x)
            except OverflowError:
                xc = x_feet
                break
            
            f_val = (y_feet - yc) * dy + (x_feet - xc)
            
            # Derivative of F(xc) with respect to xc
            # F'(xc) = (y - f)*f'' + f'*(-f') - 1
            f_prime = (y_feet - yc) * ddy - (dy * dy) - 1
            
            if abs(f_prime) < 1e-6:
                break
                
            delta = f_val / f_prime
            
            # Clamp delta
            if abs(delta) > 100:
                delta = math.copysign(100, delta)

            xc = xc - delta
            
            if abs(delta) < 0.01: # Convergence
                break

        try:
            return xc, self.catenary(xc)
        except OverflowError:
            # Fallback if final xc is bad
            return x_feet, self.catenary(x_feet)

    def get_arch_height_at_position(self, x: int) -> Optional[int]:
        """
        Get the arch height ceiling for iteration limits.
        """
        # Same as before but return a safe upper bound
        x_center_blocks = x - (self.width / 2)
        x_feet = x_center_blocks / self.girth_scale
        
        # Check bounds using design width (plus some margin for legs)
        # The legs extend BEYOND design width.
        # x_feet is feet from center.
        # Max extent is roughly 315 + 35 = 350 feet.
        if abs(x_feet) > (self.ORIGINAL_WIDTH / 2) + 50:
            return None
            
        y_feet = self.catenary(x_feet)
        
        # If x is outside the centerline span (y_feet < y_min),
        # we are potentially in the outer shell of the leg base.
        # Since the arch is nearly vertical at the base, these outer columns
        # can extend quite high. We shouldn't clamp them to 0.
        # Return full height to ensure we don't clip the leg base.
        if y_feet < self.y_min:
            return self.height
            
        y_ratio = (y_feet - self.y_min) / self.y_range
        y_blocks = int(y_ratio * self.design_height)
        
        # Add padding for the rotated triangle vertex. 
        # MUST use leg_base_width (max width) to ensure we don't clip the bottom 
        # where the leg is wide. leg_top_width is too small for the base.
        # Safety factor of 2.5x base width + extra buffer.
        return max(0, y_blocks + int(self.leg_base_width * 2.5) + 20)
    
    def get_quantized_leg_width_blocks(self, y_block: int) -> int:
        """
        Get the leg width in BLOCKS for a given Y block coordinate.
        
        This is the key anti-aliasing function: by quantizing leg width based on
        the discrete block Y-coordinate (not the continuous curve point), we ensure
        that all blocks at the same Y level use the same triangle size, eliminating
        sawtooth artifacts.
        """
        # Calculate ratio based on block coordinate
        ratio = y_block / self.design_height
        ratio = max(0.0, min(1.0, ratio))
        
        # Linear interpolation from base to top width (in blocks)
        width_blocks = self.leg_base_width - (self.leg_base_width - self.leg_top_width) * ratio
        
        # Floor to integer - this is the key quantization step
        return max(int(width_blocks), self.leg_top_width)

    def is_in_leg(self, x: int, y: int, z: int) -> bool:
        """
        Determine if a position is within the arch structure.
        Uses a true 3D distance check against the triangular cross section.
        
        Anti-aliasing: Triangle size is quantized by Y block coordinate to prevent
        sawtooth artifacts from continuous floating-point variations.
        """
        # 1. Map Block Coordinate to Feet Space
        # X and Z are centered
        x_center_block = x - (self.width / 2)
        z_center_block = z - (self.width / 2)
        
        # Y is from 0 to height
        # Convert to Y feet
        # Use design_height for ratio to preserve scale
        y_ratio = y / self.design_height
        y_feet = self.y_min + y_ratio * self.y_range
        
        # Convert X, Z to feet
        x_feet = x_center_block / self.girth_scale
        z_feet = z_center_block / self.girth_scale 
        
        # 2. Find Closest Point on Centerline Curve (xc, yc)
        # We do this for the "positive" X side (Right Leg)
        # If we are in the Left Leg (negative X), we mirror X.
        x_feet_abs = abs(x_feet)
        
        xc, yc = self.get_closest_curve_point(x_feet_abs, y_feet)
        
        # 3. Calculate Cross Section Plane Coordinates (u, v)
        # u = Normal distance in X-Y plane
        # v = Z distance (simple, as curve is planar)
        
        # Normal vector at xc: N = (-dy, 1) / sqrt(1+dy^2)
        dy = self.catenary_prime(xc)
        norm_len = math.sqrt(dy*dy + 1)
        nx = -dy / norm_len
        ny = 1.0 / norm_len
        
        # Vector from curve point to block point
        dx = x_feet_abs - xc
        dy_pt = y_feet - yc
        
        # Project onto normal
        # Note: Positive u should point OUTWARDS (away from center of curvature)
        # Center of curvature is "down". So Normal (pointing up/out) is correct.
        u = dx * nx + dy_pt * ny
        v = z_feet  # Z distance is just Z offset
        
        # 4. Triangle Check (SDF Method)
        # ANTI-ALIASING: Get leg size from BLOCK y-coordinate, not curve point
        # This ensures all blocks at the same Y level use identical triangle size,
        # eliminating sawtooth artifacts from continuous width variations.
        leg_size_blocks = self.get_quantized_leg_width_blocks(y)
        
        # Convert to feet for the SDF calculation
        block_feet = 1.0 / self.girth_scale
        leg_size = leg_size_blocks * block_feet
        
        # Define Triangle Vertices for SDF
        # Orientation: Vertex IN (negative u), Flat Side OUT (positive u)
        # Centroid at (0,0).
        # H = Altitude of equilateral triangle
        sqrt3 = 1.7320508
        H = leg_size * sqrt3 / 2.0
        
        # Flat face at u = H/3. Normal (1,0).
        # Dist1 = H/3 - u (Positive inside)
        d1 = H / 3.0 - u
        
        # Top Slant Edge: d2 = 1/2 u - sqrt3/2 v + H/3
        d2 = 0.5 * u - (sqrt3 / 2.0) * v + H / 3.0
        
        # Bottom Slant Edge (Symmetric): d3 = 1/2 u + sqrt3/2 v + H/3
        d3 = 0.5 * u + (sqrt3 / 2.0) * v + H / 3.0
        
        # Signed Distance to Triangle Boundary (Positive = Inside)
        dist = min(d1, min(d2, d3))
        
        # Outer boundary check with small margin for block coverage
        # Use 0.5 blocks - just enough to include blocks touching the surface
        outer_margin = 0.5 * block_feet
        
        if dist < -outer_margin:
            return False  # Too far outside
            
        # 5. Hollow Check
        if self.hollow:
            # Convert wall thickness from blocks to feet
            thickness_feet = self.thickness * block_feet
            
            # Add a small margin (0.5 blocks) to ensure watertight walls
            inner_margin = 0.5 * block_feet
            
            # Only hollow if we're clearly deep inside
            if dist > (thickness_feet + inner_margin):
                return False  # This block is in the hollow void
        
        return True
    
    def is_corner_block(self, x: int, y: int, z: int, neighbor_count: int) -> bool:
        """Determine if a block is on a corner/edge."""
        # Aggressive optimization: treat everything as primary block
        # Corner blocks are mostly cosmetic and expensive to calculate
        # return neighbor_count < 6
        return False
    
    def calculate_dimensions(self) -> Dict[str, Tuple[int, int, int]]:
        """Calculate estimated arch dimensions (minimal bounding box)."""
        # The arch spans design_width in X plus leg extension on each side
        # Leg extends outward by approximately 2/3 of triangle height
        leg_extension = int(self.leg_base_width * 0.6)
        
        # X dimension: design_width + 2 * leg_extension (wide, spans both legs)
        overall_width = self.design_width + 2 * leg_extension
        
        # Y dimension: design_height (base to peak)
        overall_height = self.design_height
        
        # Z dimension: THIN - just the leg width at base (widest point)
        # This is the key difference from before - Z should be small
        overall_depth = self.leg_base_width + 2
        
        # Base dimensions (each leg's cross-section at ground level)
        base_width = overall_width
        base_height = self.leg_base_width
        base_depth = self.leg_base_width
        
        # Peak dimensions (leg cross-section at top)
        peak_width = self.leg_top_width * 2  # Two legs meet
        peak_height = self.leg_top_width
        peak_depth = self.leg_top_width
        
        return {
            'base': (base_width, base_height, base_depth),
            'peak': (peak_width, peak_height, peak_depth),
            'overall': (overall_width, overall_height, overall_depth)
        }
    
    def estimate_blocks(self) -> Dict[str, int]:
        """Estimate block counts without generating full structure."""
        block_counts = Counter()
        
        # Sample every few blocks for estimation
        sample_rate = max(1, int(max(self.scale, self.girth_scale) * 5))
        
        for x in range(0, self.width, sample_rate):
            for z in range(0, self.width, sample_rate):
                arch_height = self.get_arch_height_at_position(x)
                if arch_height is None:
                    continue
                
                # Iterate with a coarser step for Y
                max_y = min(arch_height, self.height - 1)
                for y in range(0, max_y, sample_rate):
                    if self.is_in_leg(x, y, z):
                        # Simplified corner detection for estimate
                        z_center = self.width / 2
                        z_dist = abs(z - z_center)
                        leg_width = self.get_leg_width_at_height(y)
                        
                        # Edges are corners
                        if z_dist > leg_width / 2 - 2 or y < 2 or y > max_y - 2:
                            block_counts[self.corner_block] += 1
                        else:
                            block_counts[self.primary_block] += 1
        
        # Scale up estimate based on sample rate
        scale_factor = sample_rate ** 3 # 3D sampling
        return {block: count * scale_factor for block, count in block_counts.items()}
    
    def generate(self, progress_callback=None) -> LitematicaSchematic:
        """Generate the Gateway Arch schematic with minimal bounding box."""
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
                if progress_callback and current % 1000 == 0:
                    progress_callback(current, total_positions, "Calculating arch shape...")
                
                # Optimization: Check Z bounds before detailed check
                z_center = self.width / 2
                if abs(z - z_center) > self.leg_base_width + 10:
                    continue

                arch_height = self.get_arch_height_at_position(x)
                if arch_height is None:
                    continue
                
                max_y = min(arch_height, self.height - 1)
                
                for y in range(max_y + 1):
                    if self.is_in_leg(x, y, z):
                        blocks_to_place[(x, y, z)] = False
        
        # Calculate MINIMAL bounding box from actual blocks
        if not blocks_to_place:
            raise ValueError("No blocks to place - arch generation failed")
        
        min_x = min(pos[0] for pos in blocks_to_place)
        max_x = max(pos[0] for pos in blocks_to_place)
        min_y = min(pos[1] for pos in blocks_to_place)
        max_y = max(pos[1] for pos in blocks_to_place)
        min_z = min(pos[2] for pos in blocks_to_place)
        max_z = max(pos[2] for pos in blocks_to_place)
        
        # Region size is the minimal cuboid that encompasses all blocks
        region_size_x = max_x - min_x + 1
        region_size_y = max_y - min_y + 1
        region_size_z = max_z - min_z + 1
        
        # Create schematic with minimal bounds
        schematic = LitematicaSchematic()
        schematic.metadata.name = f"Gateway Arch (Scale {self.scale:.2f}×{self.girth_scale:.2f})"
        schematic.metadata.author = "TheresTheArch Generator"
        schematic.metadata.description = (
            f"Gateway Arch with accurate triangular geometry. "
            f"Height scale: {self.scale:.2f}, Width scale: {self.girth_scale:.2f}, "
            f"{'Hollow' if self.hollow else 'Solid'}, "
            f"Size: {region_size_x}×{region_size_y}×{region_size_z}, "
            f"Blocks: {self.primary_block}"
        )
        
        # Create region with MINIMAL bounding box (not a big cube)
        region = Region(
            "Arch",
            position=(0, 0, 0),
            size=(region_size_x, region_size_y, region_size_z)
        )
        
        # Pre-create block states
        primary_state = BlockState(self.primary_block)
        corner_state = BlockState(self.corner_block)
        
        # Second pass: place blocks with offset to fit minimal bounding box
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
            
            # Offset coordinates to start from (0, 0, 0)
            offset_x = x - min_x
            offset_y = y - min_y
            offset_z = z - min_z
            
            # Place appropriate block at offset position
            if self.is_corner_block(x, y, z, neighbor_count):
                region.set_block(offset_x, offset_y, offset_z, corner_state)
            else:
                region.set_block(offset_x, offset_y, offset_z, primary_state)
        
        # Add region to schematic
        schematic.add_region(region)
        
        if progress_callback:
            progress_callback(total_blocks, total_blocks, "Complete!")
        
        return schematic


# Keep the same create_simple_arch function for compatibility
def create_simple_arch(scale: float = 0.33, girth_scale: float = None, output_file: str = "gateway_arch.litematic"):
    """Create a simple Gateway Arch schematic (convenience function)."""
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
    create_simple_arch(scale=0.3, output_file="gateway_arch_accurate.litematic")

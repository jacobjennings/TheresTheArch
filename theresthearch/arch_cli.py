#!/usr/bin/env python3
"""
Gateway Arch Generator - Command Line Interface

Interactive command-line interface for generating Gateway Arch schematics.
No GUI dependencies required.
"""

import sys
import os

# Add parent directory to path to import litematica library
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'litematica-python'))

from arch_generator import ArchGenerator


def print_header():
    """Print application header."""
    print("=" * 70)
    print(" " * 15 + "GATEWAY ARCH SCHEMATIC GENERATOR")
    print("=" * 70)
    print()
    print("Generate Minecraft schematics of the Gateway Arch using the")
    print("mathematical catenary equation from the actual arch in St. Louis.")
    print()


def print_block_options():
    """Print available block types."""
    print("\nAvailable Block Types:")
    print("  1.  minecraft:quartz_block")
    print("  2.  minecraft:smooth_quartz")
    print("  3.  minecraft:white_concrete")
    print("  4.  minecraft:light_gray_concrete")
    print("  5.  minecraft:gray_concrete")
    print("  6.  minecraft:stone_bricks")
    print("  7.  minecraft:polished_andesite")
    print("  8.  minecraft:polished_diorite")
    print("  9.  minecraft:prismarine")
    print("  10. minecraft:iron_block")
    print("  11. minecraft:diamond_block")
    print("  12. minecraft:gold_block")
    print("  13. minecraft:obsidian")
    print("  14. minecraft:blackstone")
    print("  15. minecraft:deepslate_tiles")
    print("  16. Custom (enter block ID)")


def get_block_choice(prompt, allow_none=False):
    """Get block choice from user."""
    blocks = [
        "minecraft:quartz_block",
        "minecraft:smooth_quartz",
        "minecraft:white_concrete",
        "minecraft:light_gray_concrete",
        "minecraft:gray_concrete",
        "minecraft:stone_bricks",
        "minecraft:polished_andesite",
        "minecraft:polished_diorite",
        "minecraft:prismarine",
        "minecraft:iron_block",
        "minecraft:diamond_block",
        "minecraft:gold_block",
        "minecraft:obsidian",
        "minecraft:blackstone",
        "minecraft:deepslate_tiles",
    ]
    
    print_block_options()
    if allow_none:
        print("  0.  Same as primary block")
    
    while True:
        try:
            choice = input(f"\n{prompt}: ").strip()
            
            if allow_none and choice == "0":
                return None
            
            if choice == "16":
                custom = input("Enter custom block ID (e.g., minecraft:stone): ").strip()
                if custom:
                    return custom
                continue
            
            idx = int(choice) - 1
            if 0 <= idx < len(blocks):
                return blocks[idx]
            
            print("Invalid choice. Please try again.")
        except (ValueError, KeyboardInterrupt):
            print("\nInvalid input. Please enter a number.")


def get_float_input(prompt, min_val, max_val, default):
    """Get float input from user."""
    while True:
        try:
            val = input(f"{prompt} [{default}]: ").strip()
            if not val:
                return default
            
            val = float(val)
            if min_val <= val <= max_val:
                return val
            
            print(f"Value must be between {min_val} and {max_val}")
        except ValueError:
            print("Invalid number. Please try again.")
        except KeyboardInterrupt:
            print()
            sys.exit(0)


def get_int_input(prompt, min_val, max_val, default):
    """Get integer input from user."""
    while True:
        try:
            val = input(f"{prompt} [{default}]: ").strip()
            if not val:
                return default
            
            val = int(val)
            if min_val <= val <= max_val:
                return val
            
            print(f"Value must be between {min_val} and {max_val}")
        except ValueError:
            print("Invalid number. Please try again.")
        except KeyboardInterrupt:
            print()
            sys.exit(0)


def get_yes_no(prompt, default=True):
    """Get yes/no input from user."""
    default_str = "Y/n" if default else "y/N"
    while True:
        try:
            response = input(f"{prompt} [{default_str}]: ").strip().lower()
            if not response:
                return default
            if response in ['y', 'yes']:
                return True
            if response in ['n', 'no']:
                return False
            print("Please enter 'y' or 'n'")
        except KeyboardInterrupt:
            print()
            sys.exit(0)


def get_string_input(prompt, default):
    """Get string input from user."""
    try:
        val = input(f"{prompt} [{default}]: ").strip()
        return val if val else default
    except KeyboardInterrupt:
        print()
        sys.exit(0)


def show_preview(generator):
    """Show preview information."""
    print("\n" + "=" * 70)
    print(" " * 25 + "PREVIEW")
    print("=" * 70)
    
    # Dimensions
    dims = generator.calculate_dimensions()
    overall = dims['overall']
    base = dims['base']
    peak = dims['peak']
    
    print("\nDimensions:")
    print(f"  Overall: {overall[0]:>4}W × {overall[1]:>4}H × {overall[2]:>4}D blocks")
    print(f"  Base:    {base[0]:>4}W × {base[1]:>4}H × {base[2]:>4}D blocks")
    print(f"  Peak:    {peak[0]:>4}W × {peak[1]:>4}H × {peak[2]:>4}D blocks")
    
    # Estimate blocks
    print("\nEstimating block counts...")
    blocks = generator.estimate_blocks()
    
    print("\nEstimated Blocks:")
    total = sum(blocks.values())
    total_stacks = total / 64
    total_shulkers = total / (27 * 64)
    
    for block_type, count in sorted(blocks.items()):
        block_name = block_type.replace("minecraft:", "").replace("_", " ").title()
        stacks = count / 64
        shulkers = count / (27 * 64)
        print(f"\n  {block_name}:")
        print(f"    {count:>10,} blocks")
        print(f"    {stacks:>10.1f} stacks")
        print(f"    {shulkers:>10.2f} shulker boxes")
    
    print(f"\n  {'TOTAL':}")
    print(f"    {total:>10,} blocks")
    print(f"    {total_stacks:>10.1f} stacks")
    print(f"    {total_shulkers:>10.2f} shulker boxes")
    
    print("\n" + "=" * 70)


def main():
    """Main CLI application."""
    print_header()
    
    print("This tool will guide you through generating a Gateway Arch schematic.")
    print()
    
    # Quick presets
    print("Quick Presets:")
    print("  1. Small Test (scale 0.2, ~50k blocks, ~1 min)")
    print("  2. Medium (scale 0.33, ~200k blocks, ~3 min)")
    print("  3. Large (scale 0.75, ~1M blocks, ~15 min)")
    print("  4. Full Scale (scale 1.0, ~2M blocks, ~30 min)")
    print("  5. Custom Settings")
    
    try:
        preset = input("\nSelect preset [2]: ").strip()
        if not preset:
            preset = "2"
        
        if preset == "1":
            scale, girth_scale, hollow, thickness = 0.2, 0.2, True, 1
            primary = "minecraft:iron_block"
            corner = None
            output = "arch_small.litematic"
            custom = False
        elif preset == "2":
            scale, girth_scale, hollow, thickness = 0.33, 0.33, True, 1
            primary = "minecraft:iron_block"
            corner = None
            output = "arch_medium.litematic"
            custom = False
        elif preset == "3":
            scale, girth_scale, hollow, thickness = 0.75, 0.75, True, 1
            primary = "minecraft:iron_block"
            corner = None
            output = "arch_large.litematic"
            custom = False
        elif preset == "4":
            scale, girth_scale, hollow, thickness = 1.0, 1.0, True, 1
            primary = "minecraft:iron_block"
            corner = None
            output = "arch_full.litematic"
            custom = False
        else:
            custom = True
        
        if custom:
            print("\n" + "-" * 70)
            print("CUSTOM SETTINGS")
            print("-" * 70)
            
            # Scale
            print("\nHeight Scale:")
            print("  1.0 = Full size (630 blocks tall)")
            print("  0.5 = Half size (315 blocks tall)")
            print("  0.1 = Small test (63 blocks tall)")
            scale = get_float_input("Enter height scale (0.1 to 2.0)", 0.1, 2.0, 0.33)
            
            print("\nWidth Scale:")
            print("  Usually same as height for authentic arch proportions")
            print("  Increase for wider/girthier arch")
            girth_scale = get_float_input("Enter width scale (0.1 to 2.0)", 0.1, 2.0, 0.33)
            
            # Hollow
            print("\nConstruction Type:")
            hollow = get_yes_no("Create hollow interior? (saves blocks)", True)
            
            if hollow:
                thickness = get_int_input("Wall thickness in blocks (1 to 10)", 1, 10, 1)
            else:
                thickness = 1
            
            # Blocks
            print("\nBlock Selection:")
            print("-" * 70)
            primary = get_block_choice("Select primary block", allow_none=False)
            corner = get_block_choice("Select corner/edge block", allow_none=True)
            
            # Output
            print("\nOutput File:")
            output = get_string_input("Output filename", "gateway_arch.litematic")
            if not output.endswith('.litematic'):
                output += '.litematic'
        
        # Create generator
        generator = ArchGenerator(
            scale=scale,
            girth_scale=girth_scale,
            hollow=hollow,
            thickness=thickness,
            primary_block=primary,
            corner_block=corner
        )
        
        # Show preview
        show_preview(generator)
        
        # Confirm
        print()
        if not get_yes_no("Generate schematic with these settings?", True):
            print("\nCancelled.")
            return
        
        # Generate
        print("\n" + "=" * 70)
        print(" " * 25 + "GENERATING")
        print("=" * 70)
        print()
        
        def progress(current, total, message):
            percent = (current / total) * 100
            bar_length = 50
            filled = int(bar_length * current / total)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f'\r{message}: |{bar}| {percent:>5.1f}%', end='', flush=True)
        
        schematic = generator.generate(progress_callback=progress)
        print()  # New line after progress
        
        # Save
        print(f"\nSaving to {output}...")
        schematic.save(output)
        
        print("\n" + "=" * 70)
        print(" " * 25 + "SUCCESS!")
        print("=" * 70)
        print(f"\nSchematic saved to: {output}")
        print("\nTo use in Minecraft:")
        print("  1. Install Litematica mod")
        print("  2. Place file in: .minecraft/schematics/")
        print("  3. Load in-game with Litematica menu (M+S)")
        print()
        
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


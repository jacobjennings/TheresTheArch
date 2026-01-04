#!/usr/bin/env python3
"""
Basic test script for the Litematica library.

This script demonstrates creating a simple schematic.
"""

from litematica import LitematicaSchematic, Region, BlockState


def create_test_schematic():
    """Create a simple test schematic."""
    print("Creating test schematic...")
    
    # Create schematic
    schematic = LitematicaSchematic()
    schematic.metadata.name = "Test Structure"
    schematic.metadata.author = "Test Script"
    schematic.metadata.description = "A simple test structure with stone blocks"
    
    # Create a 5x5x5 region
    region = Region("TestRegion", position=(0, 0, 0), size=(5, 5, 5))
    
    # Create block states
    stone = BlockState("minecraft:stone")
    glass = BlockState("minecraft:glass")
    
    # Fill with stone
    print("Filling region with blocks...")
    for x in range(5):
        for y in range(5):
            for z in range(5):
                # Use glass on edges, stone inside
                if x == 0 or x == 4 or y == 0 or y == 4 or z == 0 or z == 4:
                    region.set_block(x, y, z, glass)
                else:
                    region.set_block(x, y, z, stone)
    
    # Add region to schematic
    schematic.add_region(region)
    
    # Print info
    print(f"Schematic: {schematic.metadata.name}")
    print(f"Author: {schematic.metadata.author}")
    print(f"Regions: {len(schematic.regions)}")
    print(f"Palette size: {len(region.palette)}")
    
    return schematic


def test_save_load(filename="test_structure.litematic"):
    """Test saving and loading a schematic."""
    print(f"\n{'='*60}")
    print("Testing save and load functionality")
    print('='*60)
    
    # Create and save
    print("\n1. Creating schematic...")
    schematic = create_test_schematic()
    
    print(f"\n2. Saving to {filename}...")
    try:
        schematic.save(filename)
        print(f"✓ Successfully saved to {filename}")
    except Exception as e:
        print(f"✗ Failed to save: {e}")
        return False
    
    # Load
    print(f"\n3. Loading from {filename}...")
    try:
        loaded = LitematicaSchematic.load(filename)
        print(f"✓ Successfully loaded")
        
        # Verify
        print("\n4. Verifying loaded data...")
        assert loaded.metadata.name == schematic.metadata.name
        assert len(loaded.regions) == len(schematic.regions)
        
        region = list(loaded.regions.values())[0]
        assert region.size == (5, 5, 5)
        assert region.position == (0, 0, 0)
        
        # Check some blocks
        center_block = region.get_block(2, 2, 2)
        corner_block = region.get_block(0, 0, 0)
        assert center_block.name == "minecraft:stone"
        assert corner_block.name == "minecraft:glass"
        
        print("✓ All verifications passed!")
        return True
        
    except Exception as e:
        print(f"✗ Failed to load or verify: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_block_access():
    """Test block get/set operations."""
    print(f"\n{'='*60}")
    print("Testing block access")
    print('='*60)
    
    region = Region("Test", position=(0, 0, 0), size=(3, 3, 3))
    
    # Test setting and getting
    stone = BlockState("minecraft:stone")
    dirt = BlockState("minecraft:dirt", {"snowy": "false"})
    
    print("\nSetting blocks...")
    region.set_block(0, 0, 0, stone)
    region.set_block(1, 1, 1, dirt)
    
    print("Getting blocks...")
    block1 = region.get_block(0, 0, 0)
    block2 = region.get_block(1, 1, 1)
    
    print(f"Block at (0,0,0): {block1}")
    print(f"Block at (1,1,1): {block2}")
    
    assert block1.name == "minecraft:stone"
    assert block2.name == "minecraft:dirt"
    assert block2.properties["snowy"] == "false"
    
    print("✓ Block access test passed!")


def test_palette():
    """Test palette management."""
    print(f"\n{'='*60}")
    print("Testing palette management")
    print('='*60)
    
    region = Region("Test", position=(0, 0, 0), size=(2, 2, 2))
    
    # Initially should have just air
    print(f"Initial palette size: {len(region.palette)}")
    assert len(region.palette) == 1
    
    # Add some blocks
    stone = BlockState("minecraft:stone")
    dirt = BlockState("minecraft:dirt")
    grass = BlockState("minecraft:grass_block")
    
    region.set_block(0, 0, 0, stone)
    print(f"After adding stone: {len(region.palette)}")
    assert len(region.palette) == 2
    
    region.set_block(0, 0, 1, dirt)
    print(f"After adding dirt: {len(region.palette)}")
    assert len(region.palette) == 3
    
    region.set_block(0, 1, 0, grass)
    print(f"After adding grass: {len(region.palette)}")
    assert len(region.palette) == 4
    
    # Setting same block type shouldn't increase palette
    region.set_block(1, 0, 0, stone)
    print(f"After adding stone again: {len(region.palette)}")
    assert len(region.palette) == 4
    
    print("✓ Palette test passed!")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("LITEMATICA PYTHON LIBRARY - BASIC TESTS")
    print("="*60)
    
    try:
        # Run tests
        test_block_access()
        test_palette()
        success = test_save_load()
        
        print(f"\n{'='*60}")
        if success:
            print("✓ ALL TESTS PASSED")
        else:
            print("✗ SOME TESTS FAILED")
        print('='*60 + "\n")
        
        return success
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"✗ TESTS FAILED WITH ERROR: {e}")
        print('='*60 + "\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)


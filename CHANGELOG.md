# Changelog

## [Unreleased]

### Fixed
- **CRITICAL: Two-Leg Architecture**: Fixed arch generation to create two separate legs instead of single centered structure
  - Previous version created one central leg (incorrect)
  - Now correctly generates left leg and right leg with gap between them
  - Matches real Gateway Arch structure with two distinct legs
  - Left leg positioned at X=0 to X=leg_width
  - Right leg positioned at X=(width-leg_width) to X=width
  - Gap in the middle where legs don't connect at base

### Added
- **Scale Lock Feature**: Checkbox to synchronize height and width sliders
  - Enabled by default for authentic arch proportions
  - Lock icon (🔒) indicates when scales move together
  - Can be unlocked for custom width-to-height ratios

### Changed
- Increased initial window size from 1000×1100 to 1000×1430 (30% taller)
- Better layout spacing for scale controls with lock checkbox

## Version 1.3.0 - Accurate Arch Geometry

### MAJOR CHANGES - Structurally Accurate Gateway Arch

**Complete redesign of arch generation algorithm to match real Gateway Arch structure:**

- **Two Distinct Legs**: Changed from radial/circular design to proper two-leg structure
  - Old: Circular/radial tube design (not accurate)
  - New: Two separate legs like the real arch
  
- **Proper Leg Geometry**:
  - Base width: 54 feet (scaled) per leg - matches real arch
  - Top width: 17 feet (scaled) per leg - matches real arch
  - Linear taper from base to top (68.5% reduction)
  - Legs oriented north-south (perpendicular to arch span)
  
- **Maintains Catenary Curve**: Vertical profile still uses accurate catenary equation
- **Better Block Estimates**: More accurate counts with stacks and shulker boxes

### Technical Details

The real Gateway Arch (visible in reference image) has:
- Two legs with triangular cross-sections
- Each leg tapers from 54 ft at base to 17 ft at top
- Legs face inward/outward, not radially

New implementation properly generates this structure using leg-based geometry instead of radial distance calculations.

See [ARCH_CHANGES.md](ARCH_CHANGES.md) for detailed technical explanation.

## Version 1.2.0 - Girth Scale & Performance

### Added
- **Independent Width Scaling**: New `girth_scale` parameter allows scaling width independently from height
  - Authentic proportions: Use same value for height and width scales
  - Wider arches: Increase width scale beyond height scale
  - Available in GUI, CLI, and Python API
- **Slider Debouncing**: Scale sliders now wait 300ms after you stop moving before updating preview
  - Eliminates lag when adjusting sliders
  - Much more responsive user experience
- **Enhanced Block Count Display**: Shows blocks in three useful formats
  - Individual blocks (e.g., 52,212 blocks)
  - Stacks (e.g., 815.8 stacks, where 1 stack = 64 blocks)
  - Shulker boxes (e.g., 30.22 shulker boxes, where 1 shulker = 27 stacks = 1,728 blocks)
  - Helps with material gathering and storage planning

### Changed
- GUI now has separate "Height Scale" and "Width Scale" sliders
- Scale labels show both scale factor and actual block dimensions
- CLI prompts for both height and width scales (defaults to same value)
- `create_simple_arch()` function accepts optional `girth_scale` parameter
- **Default block changed from Quartz to Iron Block**
- **Default wall thickness changed from 3 to 1 block**
- Corner block now defaults to "Same as Primary" (None)
- Block count displays now show breakdown by blocks/stacks/shulkers

### Technical Details
- Added `girth_scale` parameter to `ArchGenerator.__init__()`
- Width calculation uses `girth_scale` instead of `scale`
- `get_arch_y()` converts distance using `girth_scale` for proper proportions
- GUI implements debouncing with `root.after()` to cancel pending updates

## Version 1.1.0 - GUI Improvements

### Fixed
1. **Window Size**: Increased default window size from 700×800 to 1000×1100 pixels for better visibility
2. **Corner Block Dropdown**: Added `state="readonly"` to corner block dropdown to match primary block behavior
3. **Block Name Display**: Both primary and corner block dropdowns now show friendly names (e.g., "Quartz Block") instead of raw IDs (e.g., "minecraft:quartz_block")
4. **Error Handling**: Fixed NameError in threading callback by properly capturing exception variables in lambda closures
5. **Progress Callbacks**: Fixed potential variable scoping issues in progress callback lambdas

### Changed
- Description text wraplength increased from 650 to 950 to match larger window size
- Block selection dropdowns now use separate display and value variables for better UX

### Technical Details

**Error Fix**: The original code had:
```python
except Exception as e:
    self.root.after(0, lambda: self.generation_error(str(e)))
```

This caused a NameError because `e` was not properly captured in the lambda closure. Fixed to:
```python
except Exception as e:
    error_msg = str(e)
    self.root.after(0, lambda err=error_msg: self.generation_error(err))
```

The same pattern was applied to all lambda callbacks to ensure proper variable capture.

## Version 1.0.0 - Initial Release

### Added
- Gateway Arch generator with mathematically accurate catenary equation
- GUI application with Tkinter
- Command-line interface (no GUI dependencies)
- Complete Litematica Python library
- Extensive documentation (5000+ lines)
- Automated setup script
- Virtual environment support
- Block customization (15+ primary blocks, 9+ corner blocks)
- Scale control (0.1× to 2.0×)
- Hollow/solid construction options
- Live preview of dimensions and block counts
- Progress tracking during generation
- File format documentation
- Usage guide and examples

### Features
- Mathematically accurate Gateway Arch generation
- Customizable scale, blocks, and construction type
- Multi-threaded generation with progress tracking
- Litematica format support (versions 1-4)
- Read and write .litematic files
- Block entities and entities support
- Efficient bit-packed storage


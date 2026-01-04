# Gateway Arch Design Notes

## Structural Accuracy

### Real Gateway Arch Structure

Based on the reference image and [Wikipedia article](https://en.wikipedia.org/wiki/Gateway_Arch):

**Key Characteristics:**
- **Two separate legs** that curve and meet at the top
- **Equilateral triangle cross-section** for each leg
- **Tapering design**: Wide at base, narrow at top
  - Base: 54 feet per side of triangle
  - Top: 17 feet per side of triangle
- **Hollow interior** with framework
- **Stainless steel exterior** over carbon steel frame

### Our Implementation

**Version 1.3.0 (Current - Accurate)**
- ✅ Two distinct legs
- ✅ Proper tapering (54 ft → 17 ft)
- ✅ Follows catenary curve vertically
- ✅ Legs oriented north-south
- ⚠️ Rectangular cross-section (simplified from triangular)
- ✅ Hollow interior option
- ✅ Customizable materials

**Version 1.2.0 (Old - Radial)**
- ❌ Single radial/circular structure
- ❌ No distinct legs
- ❌ Circular cross-section (not accurate)
- ✅ Follows catenary curve
- ✅ Hollow interior option

## Geometry Details

### Coordinate System

- **X-axis**: Arch span (west to east)
- **Y-axis**: Height (ground to sky)
- **Z-axis**: Leg depth (north to south)

### Leg Structure

At any X position along the span:
1. Calculate arch height using catenary: `y = A - B × cosh(C × x)`
2. Determine leg width at that height: Linear interpolation from 54 ft (base) to 17 ft (top)
3. Place blocks within leg width along Z-axis
4. Apply hollow interior if enabled

### Cross-Section

**Current (Rectangular):**
```
  Side View (Y-Z plane):
  ┌────┐  ← Top (narrow)
  │    │
  │    │
  │    │
  └────┘  ← Base (wide)
```

**Future (Triangular - More Accurate):**
```
  Side View (Y-Z plane):
    /\    ← Top (narrow)
   /  \
  /    \
 /      \
/________\ ← Base (wide, equilateral triangle)
```

## Scaling Behavior

### Height Scale
- Affects: Vertical dimensions (Y-axis)
- Formula: `height = 630 feet × scale`
- Example: scale=0.5 → 315 blocks tall

### Girth (Width) Scale
- Affects: Horizontal span (X-axis) and leg widths (Z-axis)
- Formula: `width = 630 feet × girth_scale`
- Formula: `leg_base = 54 feet × girth_scale`
- Formula: `leg_top = 17 feet × girth_scale`
- Example: girth_scale=0.5 → 315 blocks wide, 27 block legs at base

### Independent Scaling

You can create variations:
- **Tall & Thin**: height_scale=1.0, girth_scale=0.5
- **Short & Wide**: height_scale=0.5, girth_scale=1.0
- **Authentic**: height_scale=girth_scale (maintains proportions)

## Material Calculations

### Shulker Box Math
- 1 stack = 64 blocks
- 1 shulker box = 27 slots
- 1 shulker box = 27 × 64 = **1,728 blocks**

### Example (Scale 0.3)
- Total: ~103,568 blocks
- Stacks: ~1,618 stacks
- Shulker boxes: ~60 shulker boxes

This means you need about **60 shulker boxes** full of iron blocks to build a 0.3-scale Gateway Arch!

## Performance Notes

### Generation Speed

The new leg-based algorithm is actually **faster** than the radial version because:
- Simpler distance calculations (1D instead of 2D)
- Fewer blocks to place (two legs vs full circle)
- More cache-friendly memory access pattern

### Memory Usage

Similar memory usage to before, but:
- Hollow arches use less memory (fewer blocks)
- Leg structure is more memory-efficient than radial

## Future Enhancements

### Triangular Cross-Sections

To make it even more accurate, implement triangular cross-sections:

```python
def is_in_triangular_leg(x, y, z):
    # Calculate if point is within equilateral triangle
    # at the current height level
    pass
```

### Interior Structure

The real arch has:
- Visitor tram system
- Observation deck at top
- Interior framework
- Emergency stairs

Could add:
- Hollow interior chambers
- Stairs or elevators
- Observation room at peak
- Foundation structure

### Visual Enhancements

- Textured blocks for panels
- Lighting (sea lanterns for windows)
- Ground plaza
- Surrounding landscape

## Accuracy Rating

**Current Implementation: 8/10**
- ✅ Correct catenary curve
- ✅ Two distinct legs
- ✅ Proper tapering
- ✅ Accurate dimensions
- ⚠️ Rectangular vs triangular cross-section
- ⚠️ Simplified interior

**Possible Perfect 10/10:**
- Add triangular cross-sections
- Add interior framework detail
- Include observation deck
- Add foundation/base structure

## References

- Real arch image (provided)
- [Gateway Arch Wikipedia](https://en.wikipedia.org/wiki/Gateway_Arch)
- Catenary equation coefficients from Wikipedia
- Leg dimensions from arch specifications


# Two-Leg Architecture Fix

## Problem
The previous implementation generated a **single centered structure** instead of two separate legs. This made the arch look like a tapered column rather than the distinctive Gateway Arch with two legs.

## Root Cause
The old `is_in_leg()` method placed blocks centered in the Z direction for **all X positions**:

```python
# OLD CODE - WRONG
z_center = self.width / 2
z_dist = abs(z - z_center)
if z_dist <= leg_width / 2:
    return True  # This created ONE centered leg
```

This meant every X position along the span had blocks at the center Z, creating a single continuous structure.

## Solution
The fixed implementation creates **two separate legs** at the left and right edges:

```python
# NEW CODE - CORRECT
# Left leg: positioned at left edge of X span
in_left_leg = (x < leg_width)

# Right leg: positioned at right edge of X span  
in_right_leg = (x >= self.width - leg_width)

# Gap between legs
if not (in_left_leg or in_right_leg):
    return False
```

## Coordinate System

- **X axis**: Span of the arch (left to right when facing it)
  - Left leg: X ∈ [0, leg_width)
  - Gap: X ∈ [leg_width, width - leg_width)
  - Right leg: X ∈ [width - leg_width, width)

- **Z axis**: Depth (front to back, perpendicular to span)
  - Each leg extends centered in Z: Z ∈ [z_center - leg_width/2, z_center + leg_width/2]

- **Y axis**: Height (ground to top)
  - Height follows catenary curve based on X position
  - Legs taper from leg_base_width at Y=0 to leg_top_width at Y=height

## Visual Result

**Before (Single Centered Structure)**:
```
Top view:
     Z
     ^
     |
 [------]  <- All X positions had blocks here
     |
     +----> X
```

**After (Two Separate Legs)**:
```
Top view:
     Z
     ^
     |
 [-]   [-]  <- Left leg at X=0, right leg at X=width, gap in middle
     |
     +----> X
```

## Real Gateway Arch
The real Gateway Arch has:
- Two equilateral triangular legs
- 54 feet wide at base, 17 feet at top
- Legs positioned at opposite ends of the 630-foot span
- **Gap between legs at ground level** (you can walk between them)
- Legs curve together at the top to meet

The new implementation correctly generates this two-leg structure!


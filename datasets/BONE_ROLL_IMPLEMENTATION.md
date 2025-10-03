# Complete Bone Roll Transformation Implementation

## Overview

This implementation applies Godot Engine's complete bone axis/roll transformation algorithm to BVH animation data. This ensures skeleton animations are correctly retargeted to match Godot's Humanoid Profile bone orientations.

## The Problem

When applying bone roll corrections, you cannot just transform the rotation data. You must also:
1. Transform the skeleton offsets (bone positions)
2. Transform all animation keyframes to match the new rest pose

Failing to do this creates a coordinate system mismatch that breaks forward kinematics.

## The Solution: Godot's Rest Fixer Algorithm

Based on `post_import_plugin_skeleton_rest_fixer.cpp`, we implement a three-step process:

### Step 1: Calculate Accumulated Rotation Diffs

For each bone in hierarchy order:
```python
if has_parent:
    diffs[bone] = new_rot.T @ diffs[parent] @ old_rot
else:
    diffs[bone] = new_rot.T @ old_rot
```

The `diffs` array accumulates rotation differences from the parent chain. This is crucial for properly transforming child bone offsets.

### Step 2: Transform Skeleton Offsets

```python
for each bone:
    if has_parent:
        new_offset = diffs[parent] @ old_offset
    else:
        new_offset = old_offset
```

Each bone's offset is transformed by its parent's accumulated rotation difference.

### Step 3: Transform Animation Keyframes

For rotation keyframes:
```python
new_quat = new_pg.T @ old_pg @ old_quat @ old_rest.T @ old_pg.T @ new_pg @ new_rest
```

Where:
- `old_pg` = old parent global rotation
- `new_pg` = new parent global rotation
- `old_rest` = old rest rotation for this bone
- `new_rest` = new rest rotation for this bone
- `old_quat` = animation rotation at this keyframe

## Implementation Files

### 1. `godot_reference_poses.py`

**Key Functions:**

- `euler_to_matrix(euler_deg, order='xyz')` - Converts Euler angles to 3x3 rotation matrix
- `matrix_to_6d(matrix)` - Converts 3x3 matrix to 6D representation (first 2 columns)
- `matrix_6d_to_matrix(vec6d)` - Recovers 3x3 matrix from 6D via Gram-Schmidt
- `get_reference_rotation(bone_name)` - Gets Godot reference pose for a bone
- `apply_complete_bone_roll_transformation(...)` - **Main algorithm implementation**

**Reference Poses:**

Contains all 56 Godot Humanoid Profile bone reference poses extracted from `skeleton_profile.cpp`. Examples:

```python
"LeftUpperArm": np.array([
    [-1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, -1.0]
])

"LeftThumbMetacarpal": np.array([
    [0.0, 0.0, -1.0],
    [-0.577, 0.816, 0.0],
    [0.816, 0.577, 0.0]
])
```

### 2. `bvh_parser.py`

**Modified `to_numpy()` method:**

When `use_6d=True` and `skeleton_type=="godot_humanoid"`:

1. Calls `apply_complete_bone_roll_transformation()` with:
   - Animation rotations: `(num_frames, num_bones, 3)` Euler angles
   - Skeleton offsets: `(num_bones, 3)`
   - Topology: `(num_bones,)` parent indices
   - Bone names: List of bone names

2. Receives back:
   - Transformed rotations: `(num_frames, num_bones, 6)` in 6D representation
   - Transformed offsets: `(num_bones, 3)`

3. Updates skeleton offsets in-place
4. Returns flattened rotations + positions

## Why 6D Rotation Representation?

**Advantages over Quaternions:**
- **Continuous**: No quaternion double-cover issue (q and -q represent same rotation)
- **Singularity-free**: No gimbal lock
- **Neural network friendly**: Gradient flow is smooth

**Format:**
- Input: First 2 columns of 3x3 rotation matrix `[r11, r21, r31, r12, r22, r32]`
- Recovery: Gram-Schmidt orthogonalization + cross product for 3rd column

## Usage Example

```python
from datasets.bvh_parser import BVH_file

# Load BVH file with Godot Humanoid skeleton
bvh = BVH_file("animation.bvh")

# Get animation data with complete bone roll transformation
# Returns: (num_frames, num_bones*6 + 3)
# - num_bones*6: 6D rotation for each bone
# - 3: root position (x, y, z)
data = bvh.to_numpy(use_6d=True)

# Skeleton offsets are now transformed to match Godot reference poses
transformed_offsets = bvh.offset  # (num_bones, 3)
```

## Testing Checklist

### Basic Functionality Tests

- [ ] Load a Godot Humanoid BVH file
- [ ] Call `to_numpy(use_6d=True)`
- [ ] Verify output shape: `(num_frames, 56*6 + 3)` = `(num_frames, 339)`
- [ ] Check that offsets were modified in `bvh.offset`

### Transformation Verification Tests

- [ ] Compare original vs transformed skeleton offsets
- [ ] Verify rotation matrices are orthonormal (det = 1, R^T @ R = I)
- [ ] Check that transformed rotations are in valid 6D format
- [ ] Verify root positions remain unchanged

### Animation Integrity Tests

- [ ] Export transformed data back to BVH
- [ ] Import into Godot Engine
- [ ] Verify animations play correctly
- [ ] Check finger articulations are preserved
- [ ] Verify no gimbal lock or flipping artifacts

### Edge Cases

- [ ] Test with rest pose (all rotations = 0)
- [ ] Test with extreme rotations (near ±180°)
- [ ] Test with bones that have identity reference poses
- [ ] Test with bones that have complex reference poses (e.g., LeftThumbMetacarpal)

## Mathematical Verification

### Rotation Matrix Properties

All rotation matrices should satisfy:
```python
R @ R.T == I  # Orthogonal
det(R) == 1   # Proper rotation (not reflection)
```

### 6D to 3x3 Recovery

```python
import numpy as np
from datasets.godot_reference_poses import matrix_to_6d, matrix_6d_to_matrix

# Test round-trip conversion
R_original = np.array([[1, 0, 0], [0, 0.707, -0.707], [0, 0.707, 0.707]])
vec6d = matrix_to_6d(R_original)
R_recovered = matrix_6d_to_matrix(vec6d)

# Should be nearly identical
assert np.allclose(R_original, R_recovered, atol=1e-6)
```

### Transformation Consistency

```python
# Old and new skeleton should have same bone chain lengths
old_bone_length = np.linalg.norm(old_offset)
new_bone_length = np.linalg.norm(new_offset)
# Lengths should be identical (only orientation changes)
assert np.isclose(old_bone_length, new_bone_length)
```

## Key Insights from Godot Source

1. **Accumulated Diffs**: The `diffs` array is essential. Each bone's diff includes all parent transformations, which is why child offsets must be transformed by parent's diff.

2. **Global Rest Transforms**: Animation keyframes are transformed using global rest poses (accumulated from root), not local rest poses.

3. **Order Matters**: Bones must be processed in hierarchy order for diffs to accumulate correctly.

4. **In-Place Modification**: The algorithm modifies skeleton structure, so offsets should be updated alongside rotations.

## Troubleshooting

### Issue: Animations look distorted
- **Cause**: Offsets not transformed, only rotations
- **Solution**: Ensure `apply_complete_bone_roll_transformation()` is used, not just `apply_bone_roll()`

### Issue: Finger animations are broken
- **Cause**: End effector definitions may be incorrect
- **Solution**: Verify all 13 end effectors in `ee_names["godot_humanoid"]` are correct

### Issue: Skeleton appears "twisted"
- **Cause**: Reference poses may not match actual Godot values
- **Solution**: Double-check reference poses against `skeleton_profile.cpp`

### Issue: Root position shifts
- **Cause**: Global transform being incorrectly applied
- **Solution**: Root positions should remain unchanged; only rotations are transformed

## Future Enhancements

1. **Position Track Transformation**: Currently only transforms rotations. Could extend to properly transform position tracks for root motion.

2. **Scale Track Support**: Add scale track transformation for complete Transform3D support.

3. **Validation Tools**: Add automated checks for rotation matrix validity and skeleton integrity.

4. **Performance Optimization**: Current implementation is O(frames × bones). Could be vectorized for better performance.

## References

- Godot Engine: `editor/import/3d/post_import_plugin_skeleton_rest_fixer.cpp`
- Godot SkeletonProfile: `scene/resources/skeleton_profile.cpp`
- 6D Rotation Paper: Zhou et al. "On the Continuity of Rotation Representations in Neural Networks"

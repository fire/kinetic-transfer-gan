# Godot Humanoid Skeleton Support for Kinetic-Transfer-GAN

## Overview

This implementation adds support for the Godot Engine Humanoid skeleton profile to kinetic-transfer-gan, preserving all 56 bones including complete finger articulation (20 finger bones total).

## What Was Implemented

### 1. Reference Pose Data (`godot_reference_poses.py`)

Created a complete lookup table of all 56 Godot Humanoid bone reference poses:
- Extracted 3x3 rotation matrices from Godot Engine's `SkeletonProfileHumanoid` class
- Each bone has its own initial orientation (bone roll) defined in the reference pose
- Implements conversion functions for bone roll correction

**Key Functions:**
- `euler_to_matrix(euler_deg, order='xyz')` - Convert Euler angles to 3x3 rotation matrix
- `matrix_to_6d(matrix)` - Convert 3x3 matrix to 6D representation (first 2 columns)
- `matrix_6d_to_matrix(vec6d)` - Recover 3x3 matrix from 6D via Gram-Schmidt
- `apply_bone_roll(euler_deg, bone_name, order='xyz')` - Apply Godot bone roll correction

**6D Representation:**
- Uses first 2 columns of rotation matrix: `[r11, r21, r31, r12, r22, r32]`
- Third column recovered via cross product after normalization
- More compact than 9 params, avoids quaternion singularities
- Continuous representation better for neural networks

### 2. Skeleton Configuration (`bvh_parser.py`)

Added Godot Humanoid to skeleton database:

**56 Bones (in order):**
```
Root, Hips, Spine, Chest, UpperChest, Neck, Head,
LeftEye, RightEye, Jaw,
LeftShoulder, LeftUpperArm, LeftLowerArm, LeftHand,
LeftThumbMetacarpal, LeftThumbProximal, LeftThumbDistal,
LeftIndexProximal, LeftIndexIntermediate, LeftIndexDistal,
LeftMiddleProximal, LeftMiddleIntermediate, LeftMiddleDistal,
LeftRingProximal, LeftRingIntermediate, LeftRingDistal,
LeftLittleProximal, LeftLittleIntermediate, LeftLittleDistal,
RightShoulder, RightUpperArm, RightLowerArm, RightHand,
RightThumbMetacarpal, RightThumbProximal, RightThumbDistal,
RightIndexProximal, RightIndexIntermediate, RightIndexDistal,
RightMiddleProximal, RightMiddleIntermediate, RightMiddleDistal,
RightRingProximal, RightRingIntermediate, RightRingDistal,
RightLittleProximal, RightLittleIntermediate, RightLittleDistal,
LeftUpperLeg, LeftLowerLeg, LeftFoot, LeftToes,
RightUpperLeg, RightLowerLeg, RightFoot, RightToes
```

**13 End Effectors:**
```
LeftToes, RightToes, Head,
LeftThumbDistal, LeftIndexDistal, LeftMiddleDistal, LeftRingDistal, LeftLittleDistal,
RightThumbDistal, RightIndexDistal, RightMiddleDistal, RightRingDistal, RightLittleDistal
```

**Skeleton Detection:**
- Detects Godot Humanoid by presence of `LeftThumbMetacarpal` and `Root` bones
- Placed first in detection order to take priority

## What Still Needs Implementation

### Critical: Bone Roll Conversion in `to_numpy()`

The `to_numpy()` method currently outputs:
- **3 Euler angle parameters per bone** (standard mode), OR
- **4 quaternion parameters per bone** (quater mode)

It needs to be modified to output:
- **6D representation parameters per bone** (for Godot Humanoid skeleton)

### Implementation Steps Needed:

1. **Import godot_reference_poses module:**
```python
from datasets.godot_reference_poses import apply_bone_roll, GODOT_REFERENCE_POSES
```

2. **Modify `to_numpy()` method:**
```python
def to_numpy(self, quater=False, edge=True, use_6d=False):
    rotations = self.anim.rotations[:, self.corps, :]
    
    # NEW: Apply bone roll correction for Godot Humanoid
    if use_6d and self.skeleton_type == "godot_humanoid":
        # Convert each bone's Euler rotation to 6D with bone roll correction
        rot_6d_list = []
        for frame_idx in range(rotations.shape[0]):
            frame_6d = []
            for bone_idx, bone_name in enumerate(self.simplified_name):
                euler = rotations[frame_idx, bone_idx, :]
                vec6d = apply_bone_roll(euler, bone_name, order='xyz')
                frame_6d.append(vec6d)
            rot_6d_list.append(np.concatenate(frame_6d))
        rotations = np.array(rot_6d_list)
    elif quater:
        rotations = Quaternions.from_euler(np.radians(rotations)).qs
    else:
        rotations = rotations.reshape(rotations.shape[0], -1)
    
    positions = self.anim.positions[:, 0, :]
    
    if edge and not use_6d:
        # Edge filtering only for non-6D mode
        index = []
        for e in self.edges:
            index.append(e[0])
        rotations = rotations[:, index, :]
        rotations = rotations.reshape(rotations.shape[0], -1)
    
    return np.concatenate((rotations, positions), axis=1)
```

3. **Update preprocessing calls:**
```python
# In datasets/preprocess.py
motion_data = bvh_file.to_numpy(quater=False, edge=True, use_6d=True)
```

4. **Update training/inference code** to handle 6D representation
- Models need to expect 6D rotation params (6 × num_bones) instead of 3D (3 × num_bones)
- Loss functions may need adjustment
- Forward kinematics may need 6D → matrix conversion

## File Structure

```
datasets/
├── godot_reference_poses.py      # NEW: Reference poses + conversion functions
├── bvh_parser.py                 # MODIFIED: Added Godot Humanoid config
├── godot_humanoid_skeleton.py    # EXISTING: Bone arrays
├── preprocess.py                 # NEEDS UPDATE: Use 6D mode
└── GODOT_HUMANOID_README.md      # THIS FILE
```

## Bone Roll Examples

Key bones with non-identity reference poses:

| Bone | Reference Pose (3x3) | Purpose |
|------|---------------------|---------|
| LeftShoulder | `[0,0,1; 1,0,0; 0,1,0]` | 90° rotation for shoulder orientation |
| LeftLowerArm | `[0,0,1; -1,0,0; 0,-1,0]` | Forearm twist alignment |
| LeftHand | `[0,0,-1; 1,0,0; 0,-1,0]` | Hand palm orientation |
| LeftThumbMetacarpal | `[0,0,-1; -0.577,0.816,0; 0.816,0.577,0]` | Thumb angle (~35°) |
| LeftUpperLeg | `[-1,0,0; 0,-1,0; 0,0,1]` | Hip rotation |
| LeftFoot | `[-1,0,0; 0,0,-1; 0,-1,0]` | Foot orientation |

Most finger bones use identity (no roll correction needed).

## Testing Plan

1. **Create test Godot Humanoid BVH file**
   - Export from Godot with full finger rig
   - Verify all 56 bones present

2. **Test BVH parser detection**
   ```python
   from datasets.bvh_parser import BVH_file
   bvh = BVH_file("path/to/godot_humanoid.bvh")
   assert bvh.skeleton_type == "godot_humanoid"
   assert len(bvh.simplified_name) == 56
   assert len(bvh.ee_id) == 13
   ```

3. **Test 6D conversion**
   ```python
   data = bvh.to_numpy(use_6d=True)
   # Should be: (num_frames, 56*6 + 3)
   # 56 bones × 6 params + 3 root position
   ```

4. **Test bone roll correction**
   ```python
   from datasets.godot_reference_poses import apply_bone_roll
   # Test known case: identity Euler should give identity 6D after roll correction
   euler_identity = np.array([0.0, 0.0, 0.0])
   vec6d = apply_bone_roll(euler_identity, "Hips")  # Hips has identity reference
   expected = np.array([1, 0, 0, 0, 1, 0])  # Identity matrix first 2 columns
   np.testing.assert_allclose(vec6d, expected, atol=1e-6)
   ```

5. **Test reconstruction**
   ```python
   from datasets.godot_reference_poses import matrix_6d_to_matrix
   # Verify we can recover the rotation matrix
   R = matrix_6d_to_matrix(vec6d)
   # Check it's orthonormal
   assert np.allclose(R @ R.T, np.eye(3))
   assert np.allclose(np.linalg.det(R), 1.0)
   ```

## Optional Bones in Godot Humanoid

**Required (17 bones):**
- Hips, Spine, Head
- LeftShoulder, LeftUpperArm, LeftLowerArm, LeftHand
- RightShoulder, RightUpperArm, RightLowerArm, RightHand  
- LeftUpperLeg, LeftLowerLeg, LeftFoot
- RightUpperLeg, RightLowerLeg, RightFoot

**Optional (39 bones):**
- Root, Chest, UpperChest, Neck
- LeftEye, RightEye, Jaw (face)
- LeftToes, RightToes
- All 20 finger bones (10 per hand)

For skeletons missing optional bones (e.g., O3DE lacks fingers):
- Could use identity/T-pose 6D representation
- Or train GAN to synthesize plausible finger motion from arm/wrist data

## References

- Godot Engine source: `scene/resources/skeleton_profile.cpp`
- 6D Rotation Representation: Zhou et al. "On the Continuity of Rotation Representations in Neural Networks" (CVPR 2019)
- Kinetic Transfer GAN: Aberman et al. "Skeleton-Aware Networks for Deep Motion Retargeting" (SIGGRAPH 2020)

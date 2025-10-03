"""
Godot Humanoid Skeleton Reference Poses

Extracted from Godot Engine's SkeletonProfileHumanoid class.
Each bone has a reference_pose Transform3D defining its rest orientation.

Transform3D format: (basis.x.x, basis.x.y, basis.x.z, basis.y.x, basis.y.y, basis.y.z, basis.z.x, basis.z.y, basis.z.z, origin.x, origin.y, origin.z)
We extract only the 3x3 basis matrix for bone roll correction.
"""

import numpy as np

# Reference pose 3x3 rotation matrices for all 56 Godot Humanoid bones
# Basis is stored in column-major format: [X-axis, Y-axis, Z-axis]
GODOT_REFERENCE_POSES = {
    "Root": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "Hips": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "Spine": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "Chest": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "UpperChest": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "Neck": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "Head": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftEye": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, -1.0, 0.0]
    ]),
    "RightEye": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, -1.0, 0.0]
    ]),
    "Jaw": np.array([
        [-1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0]
    ]),
    "LeftShoulder": np.array([
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]
    ]),
    "LeftUpperArm": np.array([
        [-1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, -1.0]
    ]),
    "LeftLowerArm": np.array([
        [0.0, 0.0, 1.0],
        [-1.0, 0.0, 0.0],
        [0.0, -1.0, 0.0]
    ]),
    "LeftHand": np.array([
        [0.0, 0.0, -1.0],
        [1.0, 0.0, 0.0],
        [0.0, -1.0, 0.0]
    ]),
    "LeftThumbMetacarpal": np.array([
        [0.0, 0.0, -1.0],
        [-0.577, 0.816, 0.0],
        [0.816, 0.577, 0.0]
    ]),
    "LeftThumbProximal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftThumbDistal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftIndexProximal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftIndexIntermediate": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftIndexDistal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftMiddleProximal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftMiddleIntermediate": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftMiddleDistal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftRingProximal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftRingIntermediate": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftRingDistal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftLittleProximal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftLittleIntermediate": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftLittleDistal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightShoulder": np.array([
        [0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]
    ]),
    "RightUpperArm": np.array([
        [-1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, -1.0]
    ]),
    "RightLowerArm": np.array([
        [0.0, 0.0, -1.0],
        [1.0, 0.0, 0.0],
        [0.0, -1.0, 0.0]
    ]),
    "RightHand": np.array([
        [0.0, 0.0, 1.0],
        [-1.0, 0.0, 0.0],
        [0.0, -1.0, 0.0]
    ]),
    "RightThumbMetacarpal": np.array([
        [0.0, 0.0, 1.0],
        [0.577, 0.816, 0.0],
        [-0.816, 0.577, 0.0]
    ]),
    "RightThumbProximal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightThumbDistal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightIndexProximal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightIndexIntermediate": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightIndexDistal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightMiddleProximal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightMiddleIntermediate": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightMiddleDistal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightRingProximal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightRingIntermediate": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightRingDistal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightLittleProximal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightLittleIntermediate": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightLittleDistal": np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftUpperLeg": np.array([
        [-1.0, 0.0, 0.0],
        [0.0, -1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "LeftLowerLeg": np.array([
        [-1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, -1.0]
    ]),
    "LeftFoot": np.array([
        [-1.0, 0.0, 0.0],
        [0.0, 0.0, -1.0],
        [0.0, -1.0, 0.0]
    ]),
    "LeftToes": np.array([
        [-1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, -1.0]
    ]),
    "RightUpperLeg": np.array([
        [-1.0, 0.0, 0.0],
        [0.0, -1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]),
    "RightLowerLeg": np.array([
        [-1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, -1.0]
    ]),
    "RightFoot": np.array([
        [-1.0, 0.0, 0.0],
        [0.0, 0.0, -1.0],
        [0.0, -1.0, 0.0]
    ]),
    "RightToes": np.array([
        [-1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, -1.0]
    ]),
}

def euler_to_matrix(euler_deg, order='xyz'):
    """
    Convert Euler angles (in degrees) to 3x3 rotation matrix.
    
    Args:
        euler_deg: Euler angles in degrees, shape (..., 3) for (X, Y, Z)
        order: Rotation order (e.g., 'xyz', 'zyx')
    
    Returns:
        3x3 rotation matrix
    """
    euler_rad = np.radians(euler_deg)
    
    if order.lower() == 'xyz':
        rx, ry, rz = euler_rad[..., 0], euler_rad[..., 1], euler_rad[..., 2]
        
        # Rotation around X
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(rx), -np.sin(rx)],
            [0, np.sin(rx), np.cos(rx)]
        ])
        
        # Rotation around Y
        Ry = np.array([
            [np.cos(ry), 0, np.sin(ry)],
            [0, 1, 0],
            [-np.sin(ry), 0, np.cos(ry)]
        ])
        
        # Rotation around Z
        Rz = np.array([
            [np.cos(rz), -np.sin(rz), 0],
            [np.sin(rz), np.cos(rz), 0],
            [0, 0, 1]
        ])
        
        # Combined rotation: Rz * Ry * Rx
        return Rz @ Ry @ Rx
    else:
        raise NotImplementedError(f"Rotation order '{order}' not implemented")


def matrix_to_6d(matrix):
    """
    Convert 3x3 rotation matrix to 6D representation.
    
    Uses first 2 columns of the matrix. The 3rd column can be recovered
    via cross product and normalization.
    
    Args:
        matrix: 3x3 rotation matrix
    
    Returns:
        6D vector: [r11, r21, r31, r12, r22, r32]
    """
    return matrix[:, :2].flatten()


def matrix_6d_to_matrix(vec6d):
    """
    Recover 3x3 rotation matrix from 6D representation.
    
    Args:
        vec6d: 6D vector [r11, r21, r31, r12, r22, r32]
    
    Returns:
        3x3 rotation matrix
    """
    vec6d = np.array(vec6d).reshape(3, 2)
    
    # Normalize first column
    col1 = vec6d[:, 0]
    col1 = col1 / np.linalg.norm(col1)
    
    # Gram-Schmidt orthogonalization for second column
    col2 = vec6d[:, 1]
    col2 = col2 - np.dot(col1, col2) * col1
    col2 = col2 / np.linalg.norm(col2)
    
    # Cross product for third column
    col3 = np.cross(col1, col2)
    
    return np.column_stack([col1, col2, col3])


def apply_bone_roll(euler_deg, bone_name, order='xyz'):
    """
    Apply bone roll correction to Euler angles for Godot Humanoid Profile.
    
    Args:
        euler_deg: Euler angles in degrees (3-element array)
        bone_name: Name of the bone (must be in GODOT_REFERENCE_POSES)
        order: Rotation order (default 'xyz')
    
    Returns:
        6D rotation representation (6-element array)
    """
    # Convert BVH Euler to rotation matrix
    R_bvh = euler_to_matrix(euler_deg, order)
    
    # Get reference pose for this bone (default to identity if not found)
    R_ref = GODOT_REFERENCE_POSES.get(bone_name, np.eye(3))
    
    # Apply similarity transformation: R_godot = R_ref @ R_bvh @ R_ref^T
    R_godot = R_ref @ R_bvh @ R_ref.T
    
    # Convert to 6D representation
    return matrix_to_6d(R_godot)


def get_reference_rotation(bone_name):
    """
    Get the reference rotation matrix for a bone.
    
    Args:
        bone_name: Name of the bone
    
    Returns:
        3x3 rotation matrix (identity if bone not in profile)
    """
    return GODOT_REFERENCE_POSES.get(bone_name, np.eye(3))


def apply_complete_bone_roll_transformation(
    rotations, offsets, topology, bone_names, order='xyz'
):
    """
    Apply complete bone roll transformation to skeleton including offsets and animations.
    
    This implements Godot's rest fixer algorithm:
    1. Calculate new target rotations from reference poses
    2. Calculate accumulated rotation diffs
    3. Transform offsets using parent's accumulated diff
    4. Transform animation rotations to match new rest
    
    Args:
        rotations: Animation rotations (num_frames, num_bones, 3) in Euler degrees
        offsets: Skeleton offsets (num_bones, 3)
        topology: Parent indices (num_bones,) where -1 is root
        bone_names: List of bone names (num_bones,)
        order: Rotation order (default 'xyz')
    
    Returns:
        tuple of (transformed_rotations_6d, transformed_offsets)
        - transformed_rotations_6d: (num_frames, num_bones, 6)
        - transformed_offsets: (num_bones, 3)
    """
    num_frames, num_bones, _ = rotations.shape
    
    # Store old rest rotations (frame 0 or could use rest pose)
    old_rest_rotations = np.array([euler_to_matrix(rotations[0, i], order) for i in range(num_bones)])
    
    # Get new target rotations from Godot reference poses
    new_rest_rotations = np.array([get_reference_rotation(bone_names[i]) for i in range(num_bones)])
    
    # Calculate accumulated diffs (following Godot's algorithm)
    diffs = np.zeros((num_bones, 3, 3))
    for bone_idx in range(num_bones):
        parent_idx = topology[bone_idx]
        new_rot = new_rest_rotations[bone_idx]
        old_rot = old_rest_rotations[bone_idx]
        
        if parent_idx >= 0:
            # diffs[bone] = new_rot^T @ diffs[parent] @ old_rot
            diffs[bone_idx] = new_rot.T @ diffs[parent_idx] @ old_rot
        else:
            # Root bone: diffs[bone] = new_rot^T @ old_rot
            diffs[bone_idx] = new_rot.T @ old_rot
    
    # Transform offsets using parent's accumulated diff
    new_offsets = offsets.copy()
    for bone_idx in range(num_bones):
        parent_idx = topology[bone_idx]
        if parent_idx >= 0:
            # Transform offset by parent's diff: new_offset = diff[parent] @ old_offset
            new_offsets[bone_idx] = diffs[parent_idx] @ offsets[bone_idx]
    
    # Calculate global rest transforms (for animation correction)
    old_global_rest = np.zeros((num_bones, 3, 3))
    new_global_rest = np.zeros((num_bones, 3, 3))
    
    for bone_idx in range(num_bones):
        parent_idx = topology[bone_idx]
        if parent_idx >= 0:
            old_global_rest[bone_idx] = old_global_rest[parent_idx] @ old_rest_rotations[bone_idx]
            new_global_rest[bone_idx] = new_global_rest[parent_idx] @ new_rest_rotations[bone_idx]
        else:
            old_global_rest[bone_idx] = old_rest_rotations[bone_idx]
            new_global_rest[bone_idx] = new_rest_rotations[bone_idx]
    
    # Transform animation rotations
    # Formula: new_rot = new_pg^T @ old_pg @ old_rot @ old_rest^T @ old_pg^T @ new_pg @ new_rest
    transformed_rotations = np.zeros((num_frames, num_bones, 6))
    
    for frame_idx in range(num_frames):
        for bone_idx in range(num_bones):
            parent_idx = topology[bone_idx]
            
            # Get rotation matrices
            old_rot_mat = euler_to_matrix(rotations[frame_idx, bone_idx], order)
            old_rest = old_rest_rotations[bone_idx]
            new_rest = new_rest_rotations[bone_idx]
            
            # Get parent global rotations
            if parent_idx >= 0:
                old_pg = old_global_rest[parent_idx]
                new_pg = new_global_rest[parent_idx]
            else:
                old_pg = np.eye(3)
                new_pg = np.eye(3)
            
            # Apply transformation: new_rot = new_pg^T @ old_pg @ old_rot @ old_rest^T @ old_pg^T @ new_pg @ new_rest
            new_rot_mat = new_pg.T @ old_pg @ old_rot_mat @ old_rest.T @ old_pg.T @ new_pg @ new_rest
            
            # Convert to 6D representation
            transformed_rotations[frame_idx, bone_idx] = matrix_to_6d(new_rot_mat)
    
    return transformed_rotations, new_offsets

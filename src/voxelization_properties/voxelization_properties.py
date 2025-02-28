import bpy
import numpy as np

def voxel_dic(octree_depth: int):
    obj = bpy.context.object
    if obj and obj.type == 'MESH':
        apply_remesh = obj.modifiers.new(name="Remesh", type="REMESH")
        apply_remesh.mode = "BLOCKS"
        apply_remesh.octree_depth = octree_depth
        apply_remesh.scale = 1.0

        bpy.ops.object.modifier_apply(modifier=apply_remesh.name)
        bpy.ops.object.mode_set(mode='EDIT')

        obj = bpy.context.object
    bpy.ops.object.mode_set(mode='OBJECT')

    voxel_dict = {}

    for i, vert in enumerate(obj.data.vertices):
        voxel_key = tuple(np.round(vert.co, decimals=10))
        voxel_dict[f"cube{i + 1}"] = voxel_key

    keys = list(voxel_dict.keys())[:2]
    v1, v2 = voxel_dict[keys[0]], voxel_dict[keys[1]]
    longitude_cube = [abs(a - b) for a, b in zip(v1, v2) if a != b]
    return voxel_dict, longitude_cube[0]
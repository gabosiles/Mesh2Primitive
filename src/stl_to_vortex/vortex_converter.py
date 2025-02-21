import bpy

def stl_to_voxels(octree_depth: int):
    obj = bpy.context.object
    if obj and obj.type == 'MESH':
        apply_remesh = obj.modifiers.new(name="Remesh", type="REMESH")
        apply_remesh.mode = "BLOCKS"
        apply_remesh.octree_depth = octree_depth
        apply_remesh.scale = 1.0

        bpy.ops.object.modifier_apply(modifier=apply_remesh.name)
        bpy.ops.object.mode_set(mode='EDIT')

    else:
        print("No REMESH found")


stl_to_voxels(5)
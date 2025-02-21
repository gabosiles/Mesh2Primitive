import bpy
import mujoco
import bmesh
import numpy as np
import os

def stl_to_blend(stl_directory: str):
    output_directory = os.path.join(os.path.dirname(stl_directory),"blend")
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(stl_directory):
        if filename.endswith(".stl"):
            stl_file_path = os.path.join(stl_directory, filename)

            blend_filename = os.path.splitext(filename)[0] + ".blend"
            blend_file_path = os.path.join(output_directory, blend_filename)

            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete(use_global=False)
            bpy.ops.wm.stl_import(filepath=stl_file_path)

            bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)

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

    #for key, voxel in voxel_dict.items():
    #    print(f"{key}: {voxel}")

    keys = list(voxel_dict.keys())[:2]
    v1, v2 = voxel_dict[keys[0]], voxel_dict[keys[1]]
    longitude_cube = [abs(a - b) for a, b in zip(v1, v2) if a != b]
    return voxel_dict, longitude_cube


def mujoco_creator(voxel_dict, size_value, stl_directory: str, scene_name: str):
    output_directory = os.path.join(os.path.dirname(stl_directory), "xml")
    os.makedirs(output_directory, exist_ok=True)
    output_file = os.path.join(output_directory, f"{scene_name}.xml")

    mj_spec = mujoco.MjSpec()
    worldbody = mj_spec.worldbody

    body = worldbody.add_body(name="parent_body", pos=[0, 0, 0])

    for name, (x, y, z) in voxel_dict.items():
        body.add_geom(
            type=mujoco.mjtGeom.mjGEOM_BOX,
            name=name,
            size=[size_value / 2, size_value / 2, size_value / 2],
            pos=[x, y, z],
            quat=[1.0, 0.0, 0.0, 0.0]
        )
    mj_model = mj_spec.compile()
    xml_string = mj_spec.to_xml()

    with open(output_file, "w") as f:
        f.write(xml_string)


def main_voxel_converter(octree_resolution, stl_directory,blend_folder: str):
    stl_to_blend(stl_directory)
    for file in os.listdir(blend_folder):
        if file.endswith(".blend"):
            blend_path = os.path.join(blend_folder, file)
            print(f"Procesando: {blend_path}")
            bpy.ops.wm.open_mainfile(filepath=blend_path)

            if bpy.context.selected_objects:
                bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]


            voxel_dict, longitude_cube = voxel_dic(octree_resolution)

            print(f"Blend file: {blend_path} example :{longitude_cube}")
            bpy.ops.wm.save_mainfile()

            scene_name = file.replace(".blend", "")
            mujoco_creator(voxel_dict, longitude_cube[0], stl_directory, scene_name)
'''

def calculate_volume_of_a_mesh(mesh):
bm = bmesh.new()
bm.from_mesh(mesh)
bmesh.ops.triangulate(bm, faces=bm.faces[:])
bm.normal_update()
volume = bm.calc_volume(signed=False)
bm.free()
return volume

def iterations_stl_to_voxels(object,octree_depth: int):
apply_remesh = object.modifiers.new(name="Remesh", type="REMESH")
apply_remesh.mode = "BLOCKS"
apply_remesh.octree_depth = octree_depth
apply_remesh.scale = 1.0  

for obj in bpy.data.objects:
value_volume = calculate_volume_of_a_mesh(obj.data)
print(obj.name,"volume is: ",value_volume)
if value_volume < (1e-5):
    iterations_stl_to_voxels(obj,7)
elif value_volume < (1e-6):
    iterations_stl_to_voxels(obj,7)
elif value_volume < (1e-7):
    iterations_stl_to_voxels(obj,6)
elif value_volume < (1e-4):
    iterations_stl_to_voxels(obj,6)
'''
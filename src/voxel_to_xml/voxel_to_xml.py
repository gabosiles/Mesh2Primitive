import bpy
import mujoco
import bmesh
import numpy as np
import os
from stl_to_blend.stl_to_blend import stl_to_blend
from voxelization_properties.voxelization_properties import voxel_dic


def main_voxel_converter(octree_resolution, stl_directory, blend_folder: str):
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
            return (voxel_dict, longitude_cube,scene_name)
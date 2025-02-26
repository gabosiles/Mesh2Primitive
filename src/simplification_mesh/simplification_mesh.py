import bpy
import os
from mujoco_generator.mujoco_generator import mujoco_creator

def simplified_mesh_properties_extraction():
    figure_mesh = {}
    i = 0
    for obj in bpy.data.objects:
        model_name = obj.name
        if obj.type == "MESH" and not model_name.startswith("Cube" or "Cylinder" or "Sphere"):
            dimensions = obj.dimensions
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
            obj.select_set(False)

            model_location = obj.location
            size_x, size_y, size_z = dimensions.x, dimensions.y, dimensions.z
            center_x, center_y, center_z = model_location.x, model_location.y, model_location.z

            figure_mesh[f"Cube_{i}"] = [
                size_x,
                size_y,
                size_z,
                center_x,
                center_y,
                center_z
            ]
        return figure_mesh

def main(stl_directory):
    "Simplified mesh is created"
    "Saved in the blender directory"
    output_directory = os.path.join(os.path.dirname(stl_directory), "blend")
    for file in os.listdir(output_directory):
        "Opens Blend file"
        simplified_directory = simplified_mesh_properties_extraction()
        scene_name = file.replace(".blend", "")
        mujoco_creator(simplified_directory, stl_directory,scene_name)


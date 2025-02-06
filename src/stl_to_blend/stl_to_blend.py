import bpy
import os

def stl_to_blend(stl_directory: str):
    output_directory = os.path.join(os.path.dirname(stl_directory),"blend")
    os.makedirs(output_directory, exist_ok=True)
    try:
        for filename in os.listdir(stl_directory):
            if filename.endswith(".stl"):
                stl_file_path = os.path.join(stl_directory, filename)

                blend_filename = os.path.splitext(filename)[0] + ".blend"
                blend_file_path = os.path.join(output_directory, blend_filename)

                bpy.ops.object.select_all(action='SELECT')
                bpy.ops.object.delete(use_global=False)
                bpy.ops.wm.stl_import(filepath=stl_file_path)

                bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)
                print(f"Processing: {stl_file_path} -> {blend_file_path}")
    except FileNotFoundError:
        return "Directory not found"
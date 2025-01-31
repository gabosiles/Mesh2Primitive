import bpy
import os

stl_directory = "./stl"
output_directory = "./blend"

os.makedirs(output_directory, exist_ok=True)

def delete_default_objects():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

for filename in os.listdir(stl_directory):
    if filename.endswith(".stl"):
        stl_file_path = os.path.join(stl_directory, filename)

        blend_filename = os.path.splitext(filename)[0] + ".blend"
        blend_file_path = os.path.join(output_directory, blend_filename)

        delete_default_objects()
        bpy.ops.import_mesh.stl(filepath=stl_file_path)

        bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)
        print(f"Processing: {stl_file_path} -> {blend_file_path}")

print("All the STL files were succesfully converted to .blend")

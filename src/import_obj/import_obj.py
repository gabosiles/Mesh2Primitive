import bpy
import os

# Ruta del archivo .obj (ajústala según tu necesidad)
input_obj_path = "/home/gsiles/Documents/mesh_to_shape/resources/output/test.obj"

# Ruta de salida para guardar el archivo .blend
output_blend_path = "/home/gsiles/Documents/mesh_to_shape/resources/output/test.blend"

# Limpia la escena eliminando todos los objetos
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

bpy.ops.wm.obj_import(
    filepath=input_obj_path,
    forward_axis='Y',  # Eje hacia adelante
    up_axis='Z'        # Eje hacia arriba
)

# Guarda el archivo Blender en la ruta de salida
bpy.ops.wm.save_as_mainfile(filepath=output_blend_path)

print(f"Archivo guardado en: {output_blend_path}")

import bpy
import numpy as np

file_path = "/home/gsiles/Documents/Multiverse-Parser/resources/output/IAIDrawerW60H53_voxelized.stl"
for armature in bpy.data.armatures:
    bpy.data.armatures.remove(armature)
for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)
for from_obj in bpy.data.objects:
    bpy.data.objects.remove(from_obj)
for material in bpy.data.materials:
    bpy.data.materials.remove(material)
for camera in bpy.data.cameras:
    bpy.data.cameras.remove(camera)
for light in bpy.data.lights:
    bpy.data.lights.remove(light)
for image in bpy.data.images:
    bpy.data.images.remove(image)
bpy.ops.wm.stl_import(filepath=file_path, up_axis='Z', forward_axis='Y')
obj = bpy.context.object
bpy.ops.object.mode_set(mode='OBJECT')
voxel_keys = []
voxel_dict = {}
for i, vert in enumerate(obj.data.vertices):
    voxel_key = [float(vert.co.x), float(vert.co.y), float(vert.co.z)]
    voxel_keys.append(voxel_key)
size_list = len(voxel_keys)
if size_list % 2 == 0:
    v1 = voxel_keys[size_list // 2]
    v2 = voxel_keys[(size_list // 2)-1]
else:
    size_list = size_list - 1
    v1 = voxel_keys[size_list // 2]
    v2 = voxel_keys[(size_list // 2) - 1]
x = v1[0] - v2[0]
y = v1[1] - v2[1]
z = v1[2] - v2[2]
longitude = None
for value in [x, y, z]:
    if value != 0:
        longitude = value
        break
cubes = []
size = [longitude, longitude, longitude]
for i in voxel_keys:
    location = i
    cubes.append((location, size))

print(cubes)



import trimesh
def trimesh_voxelization(input_stl_file: str,output_stl_file: str):
    mesh = trimesh.load_mesh(input_stl_file)
    resolution = 64
    voxelized_mesh = mesh.voxelized(pitch=mesh.bounding_box.extents.max() / resolution)
    voxel_mesh = voxelized_mesh.as_boxes()
    voxel_mesh.export(output_stl_file)

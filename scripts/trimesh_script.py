
from trimesh_coding.trimesh_coding import trimesh_voxelization

if __name__ == '__main__':
    input_path = "../resources/input/voxelization/IAIDrawerW60H26.stl"
    output_path = "../resources/output/voxelized_mesh.stl"
    trimesh_voxelization(input_path,output_path)

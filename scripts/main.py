import sys
import os

scripts_directory = os.path.dirname(os.path.abspath(__file__))
src_directory = os.path.join(scripts_directory, '../src')
src_directory = os.path.abspath(src_directory)
sys.path.append(src_directory)

from stl_to_blend import stl_to_blend
from mesh_to_shape import mesh_to_shape

if __name__ == '__main__':
    stl_directory = "../resources/input/task_board/meshes/stl"
    stl_to_blend(stl_directory)
    blend_directory = "../resources/input/task_board/meshes/blend"
    xml_read_path = "../resources/input/task_board.xml"
    xml_write_path = "../resources/output/default.xml"
    mesh_to_shape(blend_directory,xml_read_path, xml_write_path)
'''
from mesh_to_shape import mesh_to_shape
if __name__ == '__main__':
    input_mujoco_file = "/home/gsiles/Documents/mesh_to_shape/resources/input/task_board.xml"

    output_mujoco_file_overwritten = "/home/gsiles/Documents/mesh_to_shape/resources/output/task_board_overwritten.xml"
    mesh_to_shape(in_xml_path=input_mujoco_file, out_xml_path=output_mujoco_file_overwritten, overwrite=True)

    output_mujoco_file_only_primitives = "/home/gsiles/Documents/mesh_to_shape/resources/output/task_board_only_primitives.xml"
    mesh_to_shape(in_xml_path=input_mujoco_file, out_xml_path=output_mujoco_file_overwritten, overwrite=False)

'''

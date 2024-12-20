import mujoco

from mesh_to_shape import mesh_to_shape

if __name__ == '__main__':
    input_mujoco_file = "/home/gsiles/Documents/mesh_to_shape/resources/input/task_board.xml"

    output_mujoco_file_overwritten = "/home/gsiles/Documents/mesh_to_shape/resources/output/task_board_overwritten.xml"
    mesh_to_shape(in_xml_path=input_mujoco_file, out_xml_path=output_mujoco_file_overwritten, overwrite=True)

    output_mujoco_file_only_primitives = "/home/gsiles/Documents/mesh_to_shape/resources/output/task_board_only_primitives.xml"
    mesh_to_shape(in_xml_path=input_mujoco_file, out_xml_path=output_mujoco_file_overwritten, overwrite=False)
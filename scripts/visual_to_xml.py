from voxel_to_xml.voxel_to_xml import main_voxel_converter

if __name__ == '__main__':
    stl_directory = "../resources/input/visual_stl"
    blend_directory = "../resources/input/blend"
    main_voxel_converter(3,stl_directory,blend_directory)
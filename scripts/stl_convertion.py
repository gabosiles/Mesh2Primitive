import sys
import os

scripts_directory = os.path.dirname(os.path.abspath(__file__))
src_directory = os.path.join(scripts_directory, '../src')
src_directory = os.path.abspath(src_directory)
sys.path.append(src_directory)

from stl_to_blend import stl_to_blend

# Run like this blender --background --python stl_to_blend.py
if __name__ == '__main__':
    stl_directory = "../resources/input/task_board/meshes/stl"
    stl_to_blend(stl_directory)

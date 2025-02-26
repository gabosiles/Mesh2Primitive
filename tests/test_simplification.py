import itertools
import unittest

from Cython.Shadow import sizeof
from random_events.interval import closed, closed_open, SimpleInterval
from random_events.product_algebra import SimpleEvent, Event
from random_events.variable import Continuous

from voxel_to_xml.voxel_to_xml import main_voxel_converter
from mujoco_generator.mujoco_generator import mujoco_creator
import tqdm
import plotly.graph_objects as go



class SimplificationTestCase(unittest.TestCase):

    x = Continuous("x")
    y = Continuous("y")
    z = Continuous("z")

    @classmethod
    def setUpClass(cls):
        cls.dic, cls.size, cls.name_file = main_voxel_converter(4,
                             "../resources/input/voxelization/visual_stl",
                             "../resources/input/voxelization/blend")

    def test_something(self):
        cubes = []


        for cube_name, cube in tqdm.tqdm(self.dic.items()):

            x, y, z = cube
            x = x.item()
            y = y.item()
            z = z.item()

            simple_cube = SimpleEvent({
                self.x: closed_open(x - self.size/2, x + self.size/2),
                self.y: closed_open(y - self.size/2, y + self.size/2),
                self.z: closed_open(z - self.size/2, z + self.size/2)
            })
            cubes.append(simple_cube)

        event = Event(*cubes)
        event = event.simplify()
        print(event)
        fig = go.Figure(event.plot(), event.plotly_layout())
        fig.show()

        xml_dict = {}
        i = 0
        for simple_event in event.simple_sets:
            for x, y, z in itertools.product(simple_event[self.x].simple_sets, simple_event[self.y].simple_sets, simple_event[self.z].simple_sets):
                x: SimpleInterval
                y: SimpleInterval
                z: SimpleInterval

                size_x = abs(x.lower - x.upper)
                size_y = abs(y.lower - y.upper)
                size_z = abs(z.lower - z.upper)
                center_x = x.center()
                center_y = y.center()
                center_z = z.center()
                print(center_x, center_y, center_z)
                print(size_x, size_y, size_z)
                xml_dict[f"cube_{i}"] = [size_x, size_y, size_z, center_x, center_y, center_z]
                i += 1
        mujoco_creator(xml_dict,"../resources/input/voxelization/visual_stl",self.name_file)

if __name__ == '__main__':
    unittest.main()

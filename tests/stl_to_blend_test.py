import os
import unittest
from stl_to_blend import stl_to_blend

class STLconverterTest(unittest.TestCase):
    def test_stl_import(self):
        stl_dir = "../tmp/test_stl"
        out_blend_dir = stl_to_blend(stl_dir)
        self.assertTrue(out_blend_dir)

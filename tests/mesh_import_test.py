import unittest
import os
from mesh_importer import import_mesh

class MeshImporterTest(unittest.TestCase):
    def test_import(self):
        mesh_file = "abc"
        self.assertTrue(os.path.exists(mesh_file))
        out_mesh_file = import_mesh(mesh_file)
        self.assertEqual(out_mesh_file, mesh_file)



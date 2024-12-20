# Mesh2Primitive
MeshToPrimitive is a Python-based tool designed to simplify the process of converting complex 3D mesh models into optimal primitive shapes for use in robotics simulations with MuJoCo. 
The core functionality of this tool revolves around importing STL files, analyzing their geometry, and determining the best matching primitive shape—such as a box, cylinder, ellipsoid, or capsule. 
Once the optimal shape is determined, the tool generates a new representation of the model as a primitive shape, which is then stored in a dictionary and used to generate MuJoCo-compatible XML files.

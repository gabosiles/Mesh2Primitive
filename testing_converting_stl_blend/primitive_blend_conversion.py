import bpy
import bmesh
import math
import os
import mujoco

def calculate_volume_of_a_mesh(mesh):
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.triangulate(bm, faces=bm.faces[:])
        bm.normal_update()
        volume = bm.calc_volume(signed=False)
        bm.free()
        return volume
    
def create_cube(model_location,x,y,z):
        bpy.ops.mesh.primitive_cube_add(size=1, location=model_location)
        new_cube = bpy.context.object
        new_cube.scale = (x, y, z)
        return 0

def create_cylinder(model_location,radius,z):
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=model_location)
        new_cylinder = bpy.context.object
        new_cylinder.scale = (radius, radius, z/2)
        return 0
    
def create_sphere(model_location,radius):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=model_location)
        new_sphere = bpy.context.object
        new_sphere.scale = (radius, radius, radius)
        return 0
    

def create_ellipsoid(model_location,x,y,z):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=model_location)
        new_ellipsoid = bpy.context.object
        new_ellipsoid.scale = (x/2, y/2, z/2)
        new_ellipsoid.name = "Ellipsoid"
        return 0
    
def mujoco_creator(type,x,y,z):
    blend_file_path = bpy.data.filepath
    directory = os.path.dirname(blend_file_path)
    new_dir = os.path.join(directory,"converted_blend")
    blend_filename = os.path.basename(blend_file_path)
    current_dir =os.path.dirname(bpy.data.filepath)
    xml_path = os.path.join(current_dir,"default.xml")

    name,ext = os.path.splitext(blend_filename)

    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    mj_model = mujoco.MjModel.from_xml_path(xml_path)
    mj_spec = mujoco.MjSpec()


    geom = mj_spec.worldbody.add_geom(
        name='floor',
        type=mujoco.mjtGeom.mjGEOM_PLANE,
        size=[10, 10, 0.1],
        rgba=[1, 0, 0, 1],
    )

    body = mj_spec.worldbody.add_body(
        pos=[0, 0, 1],
        quat=[1, 0, 0, 0],
    )
    
    if type == 'box':
        geom = body.add_geom(
                type=mujoco.mjtGeom.mjGEOM_BOX,
                pos=[0.0, 0.0, 0.0],
                size=[x, y, z],
                rgba=[1, 1, 1, 1],
            )
    if type == 'cylinder':
        geom = body.add_geom(
                type=mujoco.mjtGeom.mjGEOM_CYLINDER,
                pos=[0.0, 0.0, 0.0],
                size=[x, z, 0],
                rgba=[1, 1, 1, 1],    
            )
    if type == 'sphere':
        geom = body.add_geom(
                type=mujoco.mjtGeom.mjGEOM_SPHERE,
                pos=[0.0, 0.0, 0.0],
                size=[x, 0, 0],
                rgba=[1, 1, 1, 1],    
            )
    if type == 'ellipsoid':
        geom = body.add_geom(
                type=mujoco.mjtGeom.mjGEOM_ELLIPSOID,
                pos=[0.0, 0.0, 0.0],
                size=[x, y, z],
                rgba=[1, 1, 1, 1],    
            )
    if type == 'capsule':
        geom = body.add_geom(
                type=mujoco.mjtGeom.mjGEOM_CAPSULE,
                pos=[0.0, 0.0, 0.0],
                size=[x, z, 0],
                rgba=[1, 1, 1, 1],    
            )
    mj_model = mj_spec.compile()
    xml_string = mj_spec.to_xml()

    with open(xml_path, "w") as f:
        f.write(xml_string)

    
for obj in bpy.data.objects:
    model_name = obj.name
    if obj.type == "MESH" and not model_name.startswith("Cube" or "Cylinder" or "Sphere"):
        dimensions = obj.dimensions
        model_location = obj.location
        volume_mesh = calculate_volume_of_a_mesh(obj.data)
        print("Volume of Mesh: ",volume_mesh)
        x_scale,y_scale,z_scale = dimensions.x,dimensions.y,dimensions.z
        
        #create_cube(model_location, x_scale, y_scale, z_scale)
        box_list = [x_scale, 
                    y_scale, 
                    z_scale, 
                    x_scale * y_scale * z_scale
                    ]
        
        cylinder_radius = (x_scale + y_scale)/4
        #create_cylinder(model_location, cylinder_radius, z_scale)
        cylinder_list = [cylinder_radius, 
                         cylinder_radius, 
                         z_scale, 
                         math.pi * (cylinder_radius**2) * (z_scale/2)
                         ]
        
        sphere_radius = (x_scale + y_scale + z_scale)/2
        #create_sphere(model_location,sphere_radius)
        sphere_list = [sphere_radius, 
                       sphere_radius, 
                       sphere_radius, 
                       (4/3) * math.pi * (sphere_radius**3)
                       ]

        #create_ellipsoid(model_location, x_scale, y_scale, z_scale)
        ellipsoid_list = [(x_scale/2),
                          (y_scale/2),
                          (z_scale/2),
                          (4/3) * math.pi * (x_scale/2) * (y_scale/2) * (z_scale/2)
                          ]
        
        capsule_list = [cylinder_radius,
                        cylinder_radius,
                        (z_scale/2),
                        ((4/3) * math.pi * (cylinder_radius**3)) + math.pi * (cylinder_radius**2) * (z_scale/2)
                        ]
        
        dicc_of_figures = { "box" : box_list, 
                            "cylinder" : cylinder_list,
                            "sphere" : sphere_list,
                            "ellipsoid" : ellipsoid_list,
                            "capsule" : capsule_list
                            }
        
        for volumes in dicc_of_figures:
            error = abs(volume_mesh - (dicc_of_figures[volumes][3]))
            dicc_of_figures[volumes].append(error)
            
        option = min(dicc_of_figures, key=lambda k: dicc_of_figures[k][4])
        lowest_error_value = dicc_of_figures[option][4]
        print(dicc_of_figures)
        print("The best figure is",option,"with an error of",lowest_error_value)
        
        mujoco_creator(option,dicc_of_figures[option][0],dicc_of_figures[option][1],dicc_of_figures[option][2])
        
        '''
        diccionary_of_figures
        
        {FIGURE : [X, Y, Z, VOLUME, ERROR]}
        
        ex:
            {'box': [0.0026868656277656555, 0.15625163912773132, 0.2894858419895172, 0.00012153401845522237, 2.9431774328138186e-06]}
        '''
        
        
    else:
        print("No mesh found, try again")

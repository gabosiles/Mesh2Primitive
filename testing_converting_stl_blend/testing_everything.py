import xml.etree.ElementTree as ET
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


def mujoco_creator(primitive_objects_db: dict, xml_path_output: str):
    #current_dir =os.path.dirname(bpy.data.filepath)
    #xml_path = os.path.join(current_dir,"default.xml")

    mj_model = mujoco.MjModel.from_xml_path(xml_path_output)
    mj_spec = mujoco.MjSpec()

    body = mj_spec.worldbody.add_body(
        pos=[0, 0, 1],
        quat=[1, 0, 0, 0],
    )
    for mesh_name, properties in primitive_objects_db.items():
        (pos_x,
         pos_y,
         pos_z, 
         quat_x,
         quat_y,
         quat_z,
         quat_w,
         object_r,
         object_g,
         object_b,
         object_a, 
         mesh_type,
         type_of_figure, 
         size_x, 
         size_y, 
         size_z, 
         object_geom_class
         ) = properties

        if type_of_figure == 'box' and not(mesh_type == None):
            geom = body.add_geom(
                    name=mesh_name,
                    type=mujoco.mjtGeom.mjGEOM_BOX,
                    size=[size_x, size_y, size_z],
                    pos=[pos_x,pos_y,pos_z],
                    rgba=[1, 1, 1, 1],
                    quat=[quat_x,quat_y,quat_z,quat_w]
                )
        elif type_of_figure == 'cylinder' and not(mesh_type == None):
            geom = body.add_geom(
                    name=mesh_name,
                    type=mujoco.mjtGeom.mjGEOM_CYLINDER,
                    size=[size_x, size_y, 0],
                    pos=[pos_x, pos_y, pos_z],
                    rgba=[1, 1, 1, 1],
                    quat=[quat_x,quat_y,quat_z,quat_w] 
                )
        elif type_of_figure == 'sphere' and not(mesh_type == None):
            geom = body.add_geom(
                    name=mesh_name,
                    type=mujoco.mjtGeom.mjGEOM_SPHERE,
                    size=[size_x, 0, 0],
                    pos=[pos_x,pos_y,pos_z],
                    rgba=[1, 1, 1, 1],
                    quat=[quat_x,quat_y,quat_z,quat_w]  
                )
        elif type_of_figure == 'ellipsoid' and not(mesh_type == None):
            geom = body.add_geom(
                    name=mesh_name,
                    type=mujoco.mjtGeom.mjGEOM_ELLIPSOID,
                    size=[size_x, size_y, size_z],
                    pos=[pos_x,pos_y,pos_z],
                    rgba=[1, 1, 1, 1],
                    quat=[quat_x,quat_y,quat_z,quat_w]   
                )
        elif type_of_figure == 'capsule' and not(mesh_type == None):
            geom = body.add_geom(
                    name=mesh_name,
                    type=mujoco.mjtGeom.mjGEOM_CAPSULE,
                    size=[size_x, size_z, 0],
                    pos=[pos_x, pos_y, pos_z],
                    rgba=[1, 1, 1, 1],
                    quat=[quat_x,quat_y,quat_z,quat_w]  
                )
        
    
    mj_model = mj_spec.compile()    
    xml_string = mj_spec.to_xml()

    with open(xml_path_output, "w") as f:
        f.write(xml_string)


def extract_characteristics():
    for obj in bpy.data.objects:
        model_name = obj.name
        if obj.type == "MESH" and not model_name.startswith("Cube" or "Cylinder" or "Sphere"):
            dimensions = obj.dimensions
            model_location = obj.location
            volume_mesh = calculate_volume_of_a_mesh(obj.data)
            x_scale,y_scale,z_scale = dimensions.x,dimensions.y,dimensions.z
            
            box_list = [x_scale, 
                        y_scale, 
                        z_scale, 
                        x_scale * y_scale * z_scale
                        ]
            
            cylinder_radius = (x_scale + y_scale)/4

            cylinder_list = [cylinder_radius, 
                            cylinder_radius, 
                            z_scale, 
                            math.pi * (cylinder_radius**2) * (z_scale/2)
                            ]
            
            sphere_radius = (x_scale + y_scale + z_scale)/2

            sphere_list = [sphere_radius, 
                        sphere_radius, 
                        sphere_radius, 
                        (4/3) * math.pi * (sphere_radius**3)
                        ]

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
            dimension_x = dicc_of_figures[option][0]
            dimension_y = dicc_of_figures[option][1]
            dimension_z = dicc_of_figures[option][2]
            volume_of_figure = dicc_of_figures[option][3]
            lowest_error_value = dicc_of_figures[option][4]
            
            return option, dimension_x, dimension_y, dimension_z, volume_of_figure, lowest_error_value
            
            '''
            diccionary_of_figures
            {FIGURE : [X, Y, Z, VOLUME, ERROR]}
            ex:
                {'box': [0.0026868656277656555, 0.15625163912773132, 0.2894858419895172, 0.00012153401845522237, 2.9431774328138186e-06]}
            '''
            
        else:
            print("No mesh found, try again")
            return None


def parse_mujoco_xml(file_path: str, valid_classes: list):
    tree = ET.parse(file_path)
    root = tree.getroot()

    geom_dict = {}

    for geom in root.iter('geom'):
        name = geom.attrib.get('name')
        mesh = geom.get("mesh")
        pos = geom.get("pos")
        quat = geom.get("quat")
        size = geom.get("size")
        rgba = geom.get("rgba")
        geom_class = geom.get("class")
        type = geom.get("type")

        if geom_class not in valid_classes:
            continue

        if pos:
            pos_x, pos_y, pos_z = map(float, pos.split())
        else:
            pos_x = pos_y = pos_z = None

        if quat:
            quat_x, quat_y, quat_z, quat_w = map(float, quat.split())
        else:
            quat_x = quat_y = quat_z = quat_w = None
        if rgba:
            r, g, b, a = map(float, rgba.split())
        else:
            r = g = b = a = None
        if size:
            try:
                size_x,size_y,size_z = map(float,size.split())
            except:
                size_x = map(float,size)
                size_y = size_z = None
        else:
            size_x = size_y = size_z = None

        if name:
            geom_dict[name] = [
                pos_x,
                pos_y,
                pos_z,
                quat_x, 
                quat_y, 
                quat_z, 
                quat_w,
                r, 
                g, 
                b,
                a,
                mesh,
                type,
                size_x,
                size_y,
                size_z,
                geom_class,
            ]
    return geom_dict


def merge_databases(figures_db, geom_data):
    for mesh, geom_details in geom_data.items():
        if mesh in figures_db:
            figures_db[mesh].extend(geom_details)
    return figures_db


def clean_merged_db(merged_db):
    cleaned_db = {}
    no_position_db = {}
    
    for mesh, details in merged_db.items():
        pos_x, pos_y, pos_z = details[7], details[8], details[9]
        
        if pos_x is None or pos_y is None or pos_z is None:
            no_position_db[mesh] = details
        else:
            cleaned_db[mesh] = details
    
    return cleaned_db, no_position_db

def main(blend_directory: str, read_xml_filepath: str, valid_classes: list,xml_path_output: str):
    figures_db = {}
    geom_data = parse_mujoco_xml(read_xml_filepath, valid_classes)


    for filename in os.listdir(blend_directory):
        if filename.endswith(".blend"):
            blend_file_path = os.path.join(blend_directory, filename)
            bpy.ops.wm.open_mainfile(filepath=blend_file_path)
            mesh_name = filename.replace(".blend", "")
            type_of_figure, dim_x, dim_y, dim_z, volume, deviation = extract_characteristics()
            figures_db[mesh_name] = [type_of_figure, dim_x, dim_y, dim_z, volume, deviation]
    
    for key,value in geom_data.items():
        if (value[12] == "mesh") and (value[13] == None) and not (value[0] == None):
            mesh_name = value[11]

            if mesh_name in figures_db:
                shape = figures_db[mesh_name][0]
                size_x = figures_db[mesh_name][1]
                size_y = figures_db[mesh_name][2]
                size_z = figures_db[mesh_name][3]

                value[12] = shape                       
                value[13] = size_x
                value[14] = size_y
                value[15] = size_z   
        else:
            value[11] = "No_mesh"
    mujoco_creator(geom_data,xml_path_output)
'''
    merged_db = merge_databases(figures_db, geom_data)
    for mesh, details in merged_db.items():
        print(f"Mesh: {mesh}")
        print(f"  [0] Figure: {details[0]} ",type(details[0]))
        print(f"  [1] X: {details[1]}",type(details[1]))
        print(f"  [2] Y: {details[2]}",type(details[2]))
        print(f"  [3] Z: {details[3]}",type(details[3]))
        print(f"  [4] Volume: {details[4]}",type(details[4]))
        print(f"  [5] Deviation: {details[5]} ",type(details[5]))
        print(f"  [6] name: {details[6]}",type(details[6]))
        print(f"  [7] pos_x: {details[7]}",type(details[7]))
        print(f"  [8] pos_y: {details[8]}",type(details[8]))
        print(f"  [9] pos_z: {details[9]}",type(details[9]))
        print(f"  [10] r: {details[10]} ",type(details[10]))
        print(f"  [11] g: {details[11]} ",type(details[11]))
        print(f"  [12] b: {details[12]} ",type(details[12]))
        print(f"  [13] a: {details[13]} ",type(details[13]))
        print(f"  [14] quat_x: {details[14]}",type(details[14]))
        print(f"  [15] quat_y: {details[15]}",type(details[15]))
        print(f"  [16] quat_z: {details[16]}",type(details[16]))
        print(f"  [17] quat_w: {details[17]}",type(details[17]))
        print(f"  [18] geom_class: {details[18]}",type(details[18]))
        print("\n")

    cleaned_db, no_position_db = clean_merged_db(merged_db)
    print("Length of cleaned_db =",len(cleaned_db))
    print("Length of no_position_db =",len(no_position_db))

    for mesh, details in cleaned_db.items():
        print(f"Mesh: {mesh}")
        print(f"  [0] Figure: {details[0]} ",type(details[0]))
        print(f"  [1] X: {details[1]}",type(details[1]))
        print(f"  [2] Y: {details[2]}",type(details[2]))
        print(f"  [3] Z: {details[3]}",type(details[3]))
        print(f"  [4] Volume: {details[4]}",type(details[4]))
        print(f"  [5] Deviation: {details[5]} ",type(details[5]))
        print(f"  [6] name: {details[6]}",type(details[6]))
        print(f"  [7] pos_x: {details[7]}",type(details[7]))
        print(f"  [8] pos_y: {details[8]}",type(details[8]))
        print(f"  [9] pos_z: {details[9]}",type(details[9]))
        print(f"  [10] r: {details[10]} ",type(details[10]))
        print(f"  [11] g: {details[11]} ",type(details[11]))
        print(f"  [12] b: {details[12]} ",type(details[12]))
        print(f"  [13] a: {details[13]} ",type(details[13]))
        print(f"  [14] quat_x: {details[14]}",type(details[14]))
        print(f"  [15] quat_y: {details[15]}",type(details[15]))
        print(f"  [16] quat_z: {details[16]}",type(details[16]))
        print(f"  [17] quat_w: {details[17]}",type(details[17]))
        print(f"  [18] geom_class: {details[18]}",type(details[18]))
        print("\n")


    mujoco_creator(cleaned_db)
'''

blend_directory = "./blend"
read_xmlfile_name = "task_board.xml"
xml_path_output = "./blend/default.xml"
valid_classes = ["task_board_collision"]
body_classes = ["task_board_main",
                "task_board_banana_plug_black_hole",
                "task_board_banana_plug_red_hole",
                "task_board_slider",
                "task_board_cable_wrap_post_left",
                "task_board_button_blue",
                "task_board_banana_pug_port",
                "task_board_banana_pug_hole",
                "task_board_m5_stick_c",
                "task_board_cable_wrap_post_right",
                "task_board_lid",
                "task_board_lid_knob",
                "task_board_button_red"
                ]
main(blend_directory,read_xmlfile_name,valid_classes,xml_path_output)

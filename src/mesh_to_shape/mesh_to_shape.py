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


def extract_characteristics():
    for obj in bpy.data.objects:
        model_name = obj.name
        if obj.type == "MESH" and not model_name.startswith("Cube" or "Cylinder" or "Sphere"):
            dimensions = obj.dimensions
            model_location = obj.location
            volume_mesh = calculate_volume_of_a_mesh(obj.data)
            x_scale, y_scale, z_scale = dimensions.x, dimensions.y, dimensions.z

            box_list = [x_scale,
                        y_scale,
                        z_scale,
                        x_scale * y_scale * z_scale
                        ]

            cylinder_radius = (x_scale + y_scale) / 4

            cylinder_list = [cylinder_radius,
                             cylinder_radius,
                             z_scale,
                             math.pi * (cylinder_radius ** 2) * (z_scale / 2)
                             ]

            sphere_radius = (x_scale + y_scale + z_scale) / 2

            sphere_list = [sphere_radius,
                           sphere_radius,
                           sphere_radius,
                           (4 / 3) * math.pi * (sphere_radius ** 3)
                           ]

            ellipsoid_list = [(x_scale / 2),
                              (y_scale / 2),
                              (z_scale / 2),
                              (4 / 3) * math.pi * (x_scale / 2) * (y_scale / 2) * (z_scale / 2)
                              ]

            capsule_list = [cylinder_radius,
                            cylinder_radius,
                            (z_scale / 2),
                            ((4 / 3) * math.pi * (cylinder_radius ** 3)) + math.pi * (cylinder_radius ** 2) * (
                                        z_scale / 2)
                            ]

            dicc_of_figures = {"box": box_list,
                               "cylinder": cylinder_list,
                               "sphere": sphere_list,
                               "ellipsoid": ellipsoid_list,
                               "capsule": capsule_list
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

            #diccionary_of_figures
            #{FIGURE : [X, Y, Z, VOLUME, ERROR]}
            #ex:
            #    {'box': [0.0026868656277656555, 0.15625163912773132, 0.2894858419895172, 0.00012153401845522237, 2.9431774328138186e-06]}
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
            quat_w, quat_x, quat_y, quat_z = map(float, quat.split())
        else:
            quat_w = quat_x = quat_y = quat_z = None
        if rgba:
            r, g, b, a = map(float, rgba.split())
        else:
            r = g = b = a = None
        if size:
            try:
                size_x, size_y, size_z = map(float, size.split())
            except:
                size_x = map(float, size)
                size_y = size_z = None
        else:
            size_x = size_y = size_z = None

        if name:
            geom_dict[name] = {
                "pos_x": pos_x,
                "pos_y": pos_y,
                "pos_z": pos_z,
                "quat_w": quat_w,  # x
                "quat_x": quat_x,  # y
                "quat_y": quat_y,  # z
                "quat_z": quat_z,  # w
                "red": r,
                "green": g,
                "blue": b,
                "a": a,
                "mesh": mesh,
                "type": type,
                "size_x": size_x,
                "size_y": size_y,
                "size_z": size_z,
                "geom_class": geom_class,
            }
    return geom_dict


def extract_body_properties(xml_path_input: str):
    tree = ET.parse(xml_path_input)
    root = tree.getroot()

    body_properties = {}

    def extract_bodies(element, parent_name=None):
        for body in element.findall("body"):
            body_name = body.get("name")
            pos = body.get("pos", "0 0 0").split()
            quat = body.get("quat", "1 0 0 0").split()
            list_of_geom = [geom.get("name") for geom in body.findall("geom")]

            body_properties[body_name] = {
                "pos": [float(pos_value) for pos_value in pos],
                "quat": [float(quat_value) for quat_value in quat],
                "listofgeom": list_of_geom,
                "parent": parent_name
            }
            extract_bodies(body, body_name)

    for worldbody in root.findall(".//worldbody"):
        extract_bodies(worldbody)

    return body_properties


def mujoco_creator(body_dict: dict, primitive_objects_db: dict, xml_path_output: str):
    mj_spec = mujoco.MjSpec()
    body_references = {}

    worldbody = mj_spec.worldbody

    for body_name, body_values in body_dict.items():
        if body_values["parent"] is None:
            body = worldbody.add_body(
                name=body_name + "_prim",
                pos=body_values["pos"],
                quat=body_values["quat"],
            )
            body_references[body_name] = body

    for body_name, body_values in body_dict.items():
        parent_name = body_values["parent"]
        if parent_name is not None:
            parent_body = body_references.get(parent_name)
            if parent_body:
                body = parent_body.add_body(
                    name=body_name + "_prim",
                    pos=body_values["pos"],
                    quat=body_values["quat"],
                )
                body_references[body_name] = body

    for body_name, body_values in body_dict.items():
        body = body_references.get(body_name)
        if body is None:
            continue
        for mesh_name in body_values["listofgeom"]:
            if mesh_name in primitive_objects_db:
                properties = primitive_objects_db[mesh_name]
                pos_x = properties["pos_x"]
                pos_y = properties["pos_y"]
                pos_z = properties["pos_z"]
                quat_w = properties["quat_w"]
                quat_x = properties["quat_x"]
                quat_y = properties["quat_y"]
                quat_z = properties["quat_z"]
                object_r = properties["red"]
                object_g = properties["green"]
                object_b = properties["blue"]
                object_a = properties["a"]
                mesh_type = properties["mesh"]
                type_of_figure = properties["type"]
                size_x = properties["size_x"]
                size_y = properties["size_y"]
                size_z = properties["size_z"]
                object_geom_class = properties["geom_class"]

                if type_of_figure == 'box' and mesh_type is not None:
                    if pos_x is None:
                        body.add_geom(
                            name=mesh_name + "_prim",
                            type=mujoco.mjtGeom.mjGEOM_BOX,
                            size=[size_x / 2, size_y / 2, size_z / 2],
                            pos=[0, 0, 0],
                            quat=[1.0, 0.0, 0.0, 0.0]
                        )
                    else:
                        body.add_geom(
                            name=mesh_name + "_prim",
                            type=mujoco.mjtGeom.mjGEOM_BOX,
                            size=[size_x / 2, size_y / 2, size_z / 2],
                            pos=[pos_x, pos_y, pos_z],
                            quat=[quat_w, quat_x, quat_y, quat_z]
                        )
                elif type_of_figure == 'cylinder' and mesh_type is not None:
                    if pos_x is None:
                        body.add_geom(
                            name=mesh_name + "_prim",
                            type=mujoco.mjtGeom.mjGEOM_CYLINDER,
                            size=[size_x / 2, size_y / 2, 0.0],
                            pos=[0.0, 0.0, 0.0],
                            quat=[1.0, 0.0, 0.0, 0.0]
                        )
                    else:
                        body.add_geom(
                            name=mesh_name + "_prim",
                            type=mujoco.mjtGeom.mjGEOM_CYLINDER,
                            size=[size_x / 2, size_y / 2, 0],
                            pos=[pos_x, pos_y, pos_z],
                            quat=[quat_w, quat_x, quat_y, quat_z]
                        )
                elif type_of_figure == 'sphere' and mesh_type is not None:
                    if pos_x is None:
                        body.add_geom(
                            name=mesh_name + "_prim",
                            type=mujoco.mjtGeom.mjGEOM_SPHERE,
                            size=[size_x / 2, 0, 0],
                            pos=[0.0, 0.0, 0.0],
                            quat=[1.0, 0.0, 0.0, 0.0]
                        )
                    else:
                        body.add_geom(
                            name=mesh_name + "_prim",
                            type=mujoco.mjtGeom.mjGEOM_SPHERE,
                            size=[size_x / 2, 0, 0],
                            pos=[pos_x, pos_y, pos_z],
                            quat=[quat_w, quat_x, quat_y, quat_z]
                        )
                elif type_of_figure == 'ellipsoid' and mesh_type is not None:
                    if pos_x is None:
                        body.add_geom(
                            name=mesh_name + "_prim",
                            type=mujoco.mjtGeom.mjGEOM_ELLIPSOID,
                            size=[size_x / 2, size_y / 2, size_z / 2],
                            pos=[0.0, 0.0, 0.0],
                            quat=[1.0, 0.0, 0.0, 0.0]
                        )
                    else:
                        body.add_geom(
                            name=mesh_name + "_prim",
                            type=mujoco.mjtGeom.mjGEOM_ELLIPSOID,
                            size=[size_x / 2, size_y / 2, size_z / 2],
                            pos=[pos_x, pos_y, pos_z],
                            quat=[quat_w, quat_x, quat_y, quat_z]
                        )
                elif type_of_figure == 'capsule' and mesh_type is not None:
                    if pos_x is None:
                        body.add_geom(
                            name=mesh_name + "_prim",
                            type=mujoco.mjtGeom.mjGEOM_CAPSULE,
                            size=[size_x / 2, size_z / 2, 0],
                            pos=[0.0, 0.0, 0.0],
                            quat=[1.0, 0.0, 0.0, 0.0]
                        )
                    else:
                        body.add_geom(
                            name=mesh_name + "_prim",
                            type=mujoco.mjtGeom.mjGEOM_CAPSULE,
                            size=[size_x / 2, size_z / 2, 0],
                            pos=[pos_x, pos_y, pos_z],
                            quat=[quat_w, quat_x, quat_y, quat_z]
                        )

    mj_model = mj_spec.compile()
    xml_string = mj_spec.to_xml()

    with open(xml_path_output, "w") as f:
        f.write(xml_string)

def update_geom_elements(xml_file, geom_data):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for mesh in root.findall(".//mesh"):
        for parent in root.findall(".//"):
            if mesh in parent:
                parent.remove(mesh)
                break

    for geom in root.findall(".//geom[@class='task_board_visual']"):
        for parent in root.findall(".//"):
            if geom in parent:
                parent.remove(geom)
                break

    for geom in root.findall(".//geom[@class='task_board_probe_visual']"):
        for parent in root.findall(".//"):
            if geom in parent:
                parent.remove(geom)
                break

    for geom in root.findall(".//geom"):
        name = geom.get("name")
        if name in geom_data:
            data = geom_data[name]
            geom.set("type", data["type"])
            if "mesh" in geom.attrib:
                del geom.attrib["mesh"]
            size_in_x = data["size_x"]
            size_in_y = data["size_y"]
            size_in_z = data["size_z"]
            geom.set("size", f"{size_in_x} {size_in_y} {size_in_z}")

    tree.write(xml_file, encoding="unicode")



def mesh_to_shape(blend_directory: str, read_xml_filepath: str, valid_classes: list, xml_path_output: str, overwrite: bool):
    figures_db = {}
    body_data = extract_body_properties(read_xml_filepath)
    geom_data = parse_mujoco_xml(read_xml_filepath, valid_classes)

    for filename in os.listdir(blend_directory):
        if filename.endswith(".blend"):
            blend_file_path = os.path.join(blend_directory, filename)
            bpy.ops.wm.open_mainfile(filepath=blend_file_path)
            mesh_name = filename.replace(".blend","")
            type_of_figure, dim_x, dim_y, dim_z, volume, deviation = extract_characteristics()
            figures_db[mesh_name] = [type_of_figure, dim_x, dim_y, dim_z, volume, deviation]

    for key, value in geom_data.items():
        if (value["type"] == "mesh") and (value["size_x"] is None):
            mesh_name = value["mesh"]

            if mesh_name in figures_db:
                shape = figures_db[mesh_name][0]
                size_x = figures_db[mesh_name][1]
                size_y = figures_db[mesh_name][2]
                size_z = figures_db[mesh_name][3]

                value["type"] = shape
                value["size_x"] = size_x
                value["size_y"] = size_y
                value["size_z"] = size_z
        else:
            value["mesh"] = "No_mesh"

    # for key, value in body_data.items():
    #    print(key)
    #    print(value)

    if overwrite is True:
        update_geom_elements(read_xml_filepath,geom_data)
    else:
        mujoco_creator(body_data, geom_data, xml_path_output)
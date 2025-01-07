import xml.etree.ElementTree as ET

def extract_xml_data(filepath: str):
    data_dict = {}
    tree = ET.parse(filepath)
    root = tree.getroot()
    for geom in root.findall(".//geom"):
        name = geom.get("name")
        mesh = geom.get("mesh")
        pos = geom.get("pos")
        rgba = geom.get("rgba")
        quat = geom.get("quat")
        geom_class = geom.get("class")

        if mesh:
            data_dict[mesh] = [
                name,
                pos,
                rgba,
                quat,
                geom_class
            ]

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

        if mesh:
            data_dict[mesh] = [
                name,       # 0
                pos_x,      # 1
                pos_y,      # 2
                pos_z,      # 3
                r,          # 4
                g,          # 5
                b,          # 6
                a,          # 7
                quat_x,     # 8
                quat_y,     # 9
                quat_z,     # 10
                quat_w,     # 11
                geom_class  # 12
            ]
        for mesh, details in data_dict.items():
            print(f"Mesh: {mesh}")
            print(f"  Name: {details[0]}")
            print(f"  Pos: {details[1]}")
            print(f"  RGBA: {details[2]}")
            print(f"  Quat: {details[3]}")
            print(f"  Class: {details[4]}")
            print("\n")
    return data_dict
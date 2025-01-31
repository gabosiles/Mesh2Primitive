import xml.etree.ElementTree as ET

tree = ET.parse("task_board.xml")
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

    if geom_class != "task_board_collision":
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

for x, details in geom_dict.items():
    print(f"name: {x}")
    print(f"  [0] pos_x: {details[0]} ")
    print(f"  [1] pos_y: {details[1]}")
    print(f"  [2] pos_z: {details[2]}")
    print(f"  [3] quat_x: {details[3]}")
    print(f"  [4] quat_y: {details[4]}")
    print(f"  [5] quat_z: {details[5]} ")
    print(f"  [6] quat_w: {details[6]}")
    print(f"  [7] r: {details[7]}")
    print(f"  [8] g: {details[8]}")
    print(f"  [9] b: {details[9]}")
    print(f"  [10] a: {details[10]} ")
    print(f"  [11] mesh: {details[11]} ")
    print(f"  [12] type: {details[12]} ")
    print(f"  [13] size_x: {details[13]} ")
    print(f"  [14] size_y: {details[14]} ")
    print(f"  [13] size_z: {details[15]} ")
    print(f"  [14] geom_class: {details[16]} ")
    print("\n")

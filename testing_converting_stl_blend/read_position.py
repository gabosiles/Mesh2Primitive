import xml.etree.ElementTree as ET

def extract_body_properties(xml_path_input: str):
    tree = ET.parse(xml_path_input)
    root = tree.getroot()


    body_properties = {}
    for body in root.findall(".//body"):
        body_name = body.get("name")
        #if body_name in body_classes:
        pos = body.get("pos", "0 0 0").split()
        quat = body.get("quat", "1 0 0 0").split()
        list_of_geom = [geom.get("name") for geom in body.findall("geom")]


        body_properties[body_name] = {
            "pos": [float(pos_value) for pos_value in pos],
            "quat": [float(quat_value) for quat_value in quat],
            "listofgeom": list_of_geom
        }
    return body_properties

xml_path = "./task_board.xml"

dic_body = extract_body_properties(xml_path)

for key,values in dic_body.items():
    print(key)
    print(values["pos"])
    print(values["quat"])
    print(values["listofgeom"])
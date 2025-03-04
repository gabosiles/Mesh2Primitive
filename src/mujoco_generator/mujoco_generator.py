import os
import mujoco

def mujoco_creator(geometry_dict, out_directory: str,name_file):
    output_directory = os.path.join(out_directory, "voxelized_xmls")
    os.makedirs(output_directory, exist_ok=True)
    output_file = os.path.join(output_directory, f"{name_file}.xml")

    mj_spec = mujoco.MjSpec()
    worldbody = mj_spec.worldbody

    body = worldbody.add_body(name="parent_body", pos=[0, 0, 0])

    for name, values in geometry_dict.items():
        size_x, size_y, size_z, center_x, center_y, center_z = values

        body.add_geom(
            type=mujoco.mjtGeom.mjGEOM_BOX,
            name=name,
            size=[size_x/2, size_y/2, size_z/2],
            pos=[center_x, center_y, center_z],
            quat=[1.0, 0.0, 0.0, 0.0]
        )
    mj_model = mj_spec.compile()
    xml_string = mj_spec.to_xml()

    with open(output_file, "w") as f:
        f.write(xml_string)
import subprocess

def apply_coacd():

    coacd_python_path = "/home/gsiles/Documents/CoACD/python/package/bin/coacd"

    input_file = "/home/gsiles/Desktop/TaskBoardMain.stl"
    # Extraer el nombre base del archivo sin la extensión

    # Ruta del archivo de salida (cambiar extensión a .obj)
    output_obj = f"/home/gsiles/Desktop/yesy.obj"

    options = ["-am", "box", "-nm", "-t", "0.1"]
    cmd = [
        "python",
        coacd_python_path,
        "-i", input_file,
        "-o", output_obj
    ] + options

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing CoACD: {e}")
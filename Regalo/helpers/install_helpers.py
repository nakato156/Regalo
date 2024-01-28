import os
from pathlib import Path
import subprocess

def copiar_exe(path_exe, path_destino):
    total_size = os.path.getsize(path_exe)
    total_copiado = 0
    with open(path_exe, 'rb') as src_file:
        with open(path_destino, 'wb') as dest_file:
            while chunk := src_file.read(8192):
                    dest_file.write(chunk)
                    total_copiado += len(chunk)
                    yield total_copiado * 100 / total_size

def agregar_al_Path(path_instalacion:Path) -> tuple[bool, str]:
    # Obtén el valor actual de la variable PATH
    current_path = subprocess.check_output('echo %PATH%', shell=True, text=True).strip()

    # Verifica si el directorio ya está en la variable PATH
    if str(path_instalacion) not in current_path:
        # Agrega el directorio al PATH usando subprocess
        cmd = f'SETX PATH "%PATH%;{path_instalacion}"'
        try:
            subprocess.run(cmd, check=True, shell=True)
            return True, f'Ruta {path_instalacion} agregada al PATH correctamente.'
        except subprocess.CalledProcessError as e:
            False, f'Error al agregar la ruta al PATH: {e.returncode}'
    else:
        False, f'La ruta {path_instalacion} ya está presente en el PATH.'
import os
from pathlib import Path

def copiar_exe(path_exe, path_destino):
    total_size = os.path.getsize(path_exe)
    total_copiado = 0
    with open(path_exe, 'rb') as src_file:
        with open(path_destino, 'wb') as dest_file:
            while chunk := src_file.read(8192):
                    dest_file.write(chunk)
                    total_copiado += len(chunk)
                    yield total_copiado * 100 / total_size

def agregar_al_Path(path_instalacion:Path):
    os.system(f'SETX PATH %PATH%;"{path_instalacion}"')
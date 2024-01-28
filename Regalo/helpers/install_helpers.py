import os
from pathlib import Path
from subprocess import Popen

def copiar_exe(path_exe, path_destino):
    total_size = os.path.getsize(path_exe)
    total_copiado = 0
    with open(path_exe, 'rb') as src_file:
        with open(path_destino, 'wb') as dest_file:
            while chunk := src_file.read(8192):
                    dest_file.write(chunk)
                    total_copiado += len(chunk)
                    yield total_copiado * 100 / total_size

def agregar_al_Path(path_instalacion:Path) -> bool:
    comando = f'SETX PATH %PATH%;"{path_instalacion}"'
    proceso = Popen(comando, shell=True)

    # Esperar a que el proceso termine y obtener el código de retorno
    codigo_retorno = proceso.wait()

    return codigo_retorno == 0
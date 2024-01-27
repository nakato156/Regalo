# Regalo

Regalo provee una insterfaz de usuario para instalar cualquier archivo ejecutable (.exe) para windows. `Regalo` sirve para crear un instalador para tus ejecutables de forma rápida y sencilla basado en `flet`.

## Funcionamiento
Regalo proporciona una interfaz y funciones predefinidas para cada paso de la instalación (páginas).

Si conoces sobre flet o quieres una mayor personalización tendrás que crear funciones que representarán a cada página o etapa. Ejemplo:

```python
import flet as ft
from Regalo import Regalo, Controles, InstallerVars

def bienvenida(page: ft.Page, controles:Controles, varsInstal:InstallerVars) -> tuple:
    txt_titulo = ft.Text("Bienvenido a Regalo", size=18)
    
    contenido = ft.Column(
        height=200,
        controls=[
            ft.Container(
                ft.Text("Bienvenido a Regalo, una forma sencilla de crear instaladores para tus ejecutables! Espero lo disfrutes"),
                alignment=ft.alignment.top_left,
            )
        ],
    )

    btn_next = controles.next
    btn_next.current.on_click = lambda _: page.go("/paginaInstalacion")

    return (
        ft.Row([ txt_titulo ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(contenido, border=ft.border.all(1)),
        ft.Row([ btn_accept ])
    )
```
Todas las funciones reciben 3 argumentos y devuleven una tupla de elementos de flet. El primer argumento que es `page` hace referencia al objeto `page` de flet, que es la propia app o página que flet crea, el siguiente argumento son los controles y que quiere decir con esto?

-------------

## Controles

Regalo proporciona una forma sencilla de ir a las siguientes etapas de la instalación, ya sea seguir a delante, regresar, cerrar el instalador o iniciar la instalación, esto se logra mediante los `Controles` que son esos botones por defecto que proporciona regalo que son:

- `next`: Boton para ir a la siguiente página
- `back`: Boton para regresar a la página anterior
- `cancel`: Boton para cerrar el instalador
- `install`: Boton para empezar con el procedimiento de instalación

Estos controles son totalmente personalizables, se puede cambiar texto que aparece en el boton, se pueden agregar o quitar botones y modificar el funcionamientos de estos, todo esto puede ser especificado tanto al iniciar instanciar la clase `Regalo` o modificar durante la ejecución del instalador.

Los controles establecidos para el instalador se encuentran en el atributo `controles_inst` de la clase `Regalo` que es una instancia de la clase `Controles`, por lo que puedes modificar esa instancia agregando o quitando controles o reemplazando la instancia por otra. 

La clase `Controles` provee métodos para el manejo de los controles, por defecto trae un soporte para botones y progressbar con sus métodos:

### `Controles.get_btn(self, id: str) -> flet.Ref[flet.ElevatedButton]`

Método que devuelve una referencia (Ref) a un botón elevado (ElevatedButton) almacenado en el diccionario de botones (botones) de la instancia de la clase Controles. El botón es identificado por su id. Esta referencia permite acceder y manipular el botón correspondiente.

Parámetros:

- `id (str)`: Identificador único del botón.

Retorno:

- `flet.Ref[flet.ElevatedButton]`: Referencia al botón correspondiente.

### `Controles.agregar_boton(self, id, texto, **kwargs:dict)`

Método que agrega un nuevo botón (ElevatedButton) a la instancia de la clase Controles. El botón es identificado por su id y se crea con el texto proporcionado y cualquier argumento adicional especificado en el diccionario kwargs.

- `id`: Identificador único del nuevo botón.
- `texto`: Texto que se mostrará en el botón.
- `**kwargs (dict)`: Argumentos adicionales para la configuración del botón.

### `Controles.get_control(self, id: str) -> flet.Ref[Any]`

Método que devuelve una referencia (Ref) a un control agregado, ya sea un boton, progressbar u otro. Esta referencia permite acceder y manipular el control correspondiente.

Parámetros:

`id (str)`: Identificador único de la barra de progreso.

Retorno:

- `flet.Ref[Any]`: Referencia a un control.


### `Controles.agregar_pb(self, id)`

Método que agrega una nueva barra de progreso (ProgressBar) a la instancia de la clase Controles. La barra de progreso es identificada por su id.

Parámetros:

`id`: Identificador único de la nueva barra de progreso.

Retorno:

`flet.ProgressBar`: Objeto de la barra de progreso recién creado.

### `Controles.eliminar_control(self, id)`
Método que elimina un control, ya sea un botón elevado o una barra de progreso, de la instancia de la clase Controles. El control a eliminar se identifica por su id.

Parámetros:

`id`: Identificador único del control a eliminar.

Para crear el instalador se debe llamar a la clase `Regalo` y como argumentos debe recibir el nombre de tu aplicación, el path del archivo `.exe`, las páginas que representa las etapas de la instalación como una página individual de flet:

## Páginas
Las páginas o etapas son los pasos de instalación que se muestran al instalar un programa, estas páginas se pueden configurar, puedes añadir, quitar o modificar, todo esto con ayuda de `flet`. Si no conoces, no dominas o la pereza te controla puedes usar las funciones predeterminadas.

### Nota:
Todas estas funciones predeterminadas retornan una tupla y estas funciones deben ser usadas dentro de otra función que representará a la página, ejemplo:

```python
def main(page: ft.Page, controles:Controles, varsInstal:InstallerVars) -> tuple:
    componentes = funcion_predeterminada_regalo(*args)
    return componentes
    # se puede hacer directamente:
    # return funcion_predeterminada_regalo(*args)

paginas = Paginas({'/inicio':main})
```

### `def terminos_condiciones(page, controles, titulo:str, file:TextIOWrapper, txt_aceptar:str, sig_ruta:str) -> tuple`
Genera una interfaz para visualizar términos y condiciones.

Parámetros:

- `page (Page)`: Página actual de la aplicación.
- `controles (Controles)`: Controles de la aplicación.
- `titulo (str)`: Título de la sección de términos y condiciones.
- `file (TextIOWrapper)`: Archivo de texto con los términos y condiciones.
- `txt_aceptar (str)`: Texto del checkbox de aceptación.
- `sig_ruta (str)`: Ruta a la siguiente sección en caso de aceptación.

Retorno:

- `(tuple)`: Contiene la interfaz generada para la sección de términos y condiciones.

### `def config_instalacion(page, controles, varsInstal, titulo, text_seleccionar_carpeta, text_info, text_cambiar_ruta, text_expacio:str, sig_ruta:str) -> tuple`

Genera una interfaz para la sección de instalación.

Parameters:

- `page (Page)`: Página actual de la aplicación.
- `controles (Controles)`: Controles de la aplicación.
- `varsInstal (InstallerVars)`: Variables relacionadas con la instalación.
- `titulo (str)`: Título de la sección de instalación.
- `text_seleccionar_carpeta (str)`: Texto para la selección de carpeta.
- `text_info (str)`: Información adicional.
- `text_cambiar_ruta (str)`: Texto para cambiar la ruta de instalación.
- `text_expacio (str)`: Texto que muestra el espacio disponible.
- `sig_ruta (str)`: Ruta a la siguiente sección.

Returns:

- `tuple`: Contiene la interfaz generada para la sección de instalación.

### `def config(page, controles, varsInstal, titulo, txt_btn_instalar:str, txt_checkbox_path, msg_agregar_path, variable_agregar_path, sig_ruta:str) -> tuple`

Genera una interfaz para la configuración antes de la instalación.

Parameters:

- `page (Page)`: Página actual de la aplicación.
- `controles (Controles)`: Controles de la aplicación.
- `varsInstal (InstallerVars)`: Variables relacionadas con la instalación.
- `titulo (str)`: Título de la sección de configuración.
- `txt_btn_instalar (str)`: Texto del botón de instalación.
- `txt_checkbox_path (str)`: Texto del checkbox de agregar al PATH.
- `msg_agregar_path (str)`: Mensaje informativo sobre agregar al PATH.
- `variable_agregar_path (str)`: Variable que indica si agregar al PATH.
- `sig_ruta (str)`: Ruta a la siguiente sección.

Returns:

- `tuple`: Contiene la interfaz generada para la sección de configuración.

### `def instalacion(page, controles, id_btn_back, id_btn_install, pbRef:ft.Ref[ft.ProgressBar], msg_progreso) -> None`

Esta función no retorna una tupla. La función de instalación debe ser implementada por el usuario.

Parameters:
- `page (Page)`: Página actual de la aplicación.
- `controles (Controles)`: Controles de la aplicación.
- `id_btn_back (str)`: Identificador del botón de retroceso.
- `id_btn_install (str)`: Identificador del botón de instalación.
- `pbRef (ft.Ref[ft.ProgressBar])`: Referencia a la barra de progreso.
- `msg_progreso (str)`: Mensaje de progreso de instalación.

- Ejemplo de implementación:

```python
def pag_instalar(page: ft.Page, controles:Controles, varsInstal:InstallerVars) -> tuple:
    pbRef = controles.get_control("pb")

    instalacion(page, controles, varsInstal, "back", "install", pbRef, "Instalando...")

    # desactivamos la opcion de cancelar
    controles.cancel.current.visible = False
    # regalo es una instancia de la clase Regalo que proporciona la función por defecto instalar_regalo
    # se le pasa la progressbar y la ruta donde se debe instalar el programa (hecho en pasos anteriores)
    regalo.instalar_regalo(pbRef.current, varsInstal.path_instalacion) 
    # Se agrega el boton para cerrar el instalador
    controles.agregar_boton("fin", "Cerrar", on_click=lambda _: page.window_destroy())
    # Se muestra un mensaje satisfactorio
    # Tambien se puede realizar una comprobación para saber si fue todo correcto
    return (ft.Text("Instalación finalizada", size=18), ft.Text("El programa se ha instalado correctamente", size=14))

paginas = Paginas({'/instalacion': pag_instalar})
```

## Ejemplo de uso
```python
from Regalo import Regalo, Paginas, Controles, InstallerVars
from Regalo import helpers

from pathlib import Path
from os import environ

import flet as ft
from elevate import elevate

def main(page: ft.Page, controles:Controles, varsInstal:InstallerVars) -> tuple:
    txt_titulo_terminos = ft.Text("Terminos y condiciones", size=18)
    terminos_condiciones = ft.Text(open("terminos_condiciones.txt", "r").read(), size=14)
    controles.next.current.disabled = True
    
    contenido_term_cond = ft.Column(
        height=200,
        scroll=ft.ScrollMode.ALWAYS,
        controls=[
            ft.Container(
                terminos_condiciones,
                alignment=ft.alignment.top_left,
            )
        ],
    )

    def habilitar_next(e):
        btn_next.current.disabled = not btn_accept.value
        page.update()

    btn_accept = ft.Checkbox(label="Acepto los terminos y condiciones", on_change=habilitar_next)
    btn_next = controles.next
    btn_next.current.on_click = lambda _: page.go("/pathInstall")

    return (
        ft.Row([ txt_titulo_terminos ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(contenido_term_cond, border=ft.border.all(1)),
        ft.Row([ btn_accept ])
    )

def pag_config_inst(page: ft.Page, controles:Controles, varsInstal:InstallerVars) -> tuple:
    if controles["install"]:
        controles.install.current.visible = False
    controles.next.current.visible = True
    controles.next.current.disabled = False
    controles.next.current.on_click = lambda _: page.go("/config")

    def select_file(e: ft.FilePickerResultEvent):
        filepicker.get_directory_path("Selecciona la carpeta...")

    def return_path(e: ft.FilePickerResultEvent): 
        if not e.path: return
        varsInstal.path_instalacion = e.path
        directory_path.value = e.path
        directory_path.update()
    
    directory_path = ft.Text(value=varsInstal.path_instalacion, expand=1)
    filepicker = ft.FilePicker(on_result=return_path)
    
    controles.appbar.title= ft.Text("Instalación")
    return (
        ft.Text("El prgrama se instalará en la siguiente carpeta", size=16),
        ft.Text("Si desea seleccionar una carpeta, haga clic en el icono de la carpeta.", size=14),
        ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(icon=ft.icons.FOLDER_OPEN, bgcolor=ft.colors.PURPLE_700, on_click=select_file),
                    filepicker,
                    directory_path
                ], 
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=10,
            height=140,
            alignment=ft.alignment.top_left
        ),
        ft.Row([
            ft.Text(f"Se requiere al menos {helpers.get_format_size(varsInstal.path_instalador)} de espacio en disco", size=15),
        ])
    )

def pag_config(page: ft.Page, controles:Controles, varsInstal:InstallerVars) -> tuple:
    controles.appbar.title = ft.Text("Configuración")

    controles.agregar_boton("install", "Install", on_click=lambda _: page.go("/instalar"))
    controles.next.current.visible = False

    def agregar_al_Path(e):
        if not agregar_path.value: return
        varsInstal["agregar_path"] = True
    
    agregar_path = ft.Checkbox(label="Agregar al PATH", on_change=agregar_al_Path)
    return (
        ft.Text("Desea agregar el comando ktw al path?", size=18),
        agregar_path
    )

def pag_instalar(page: ft.Page, controles:Controles, varsInstal:InstallerVars) -> tuple:
    controles.appbarRef.current.visible = False
    controles.eliminar_control("back")
    controles.eliminar_control("install")
    
    pbRef = controles.get_control("pb")
    page.views.append(
        ft.View(
            page.route,
            [
                controles.appbarRef.current,
                ft.Column([ft.Text("Instalando...", size=15), ft.ProgressBar(ref=pbRef, width=500)]),
            ]
        )
    )
    
    page.update()
    controles.cancel.current.visible = False
    regalo.instalar_regalo(pbRef.current, varsInstal.path_instalacion)
    controles.agregar_boton("fin", "Cerrar", on_click=lambda _: page.window_destroy())
    return (ft.Text("Instalación finalizada", size=18), ft.Text("El programa se ha instalado correctamente", size=14))

def config(page:ft.Page, controles:Controles, varsInstal:InstallerVars):
    controles.appbarRef.current.bgcolor = ft.colors.BLUE_600

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 550 
    page.window_height = 400
    page.window_resizable = False 
    page.window_maximizable = False
    page.window_center()

    page.title = "Ktw installer"

paginas = Paginas({'/pathInstall':pag_config_inst, '/config':pag_config, "/instalar":pag_instalar})

path_ktw = Path(__file__).parent / "app.exe"

vars_config = { 
    "path_instalacion": Path(environ["USERPROFILE"]) / "KTW",
    "path_instalador": path_ktw,
    "agregar_path": False,
    "instalacion_terminada": False,
}

if __name__ == "__main__":
    elevate(show_console=False)
    regalo = Regalo("ktw", path_ktw, paginas, vars_config, func_config=config)
    regalo.abrir(main)
```


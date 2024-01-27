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
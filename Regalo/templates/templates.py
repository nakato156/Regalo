import flet as ft
from io import TextIOWrapper
from Regalo.helpers import helpers

def terminos_condiciones(page, controles, titulo:str, file:TextIOWrapper, txt_aceptar:str, sig_ruta:str) -> tuple:
    """
    Genera una interfaz para visualizar términos y condiciones.

    Parameters:
    - page: Página actual de la aplicación.
    - controles: Controles de la aplicación.
    - titulo: Título de la sección de términos y condiciones.
    - file: Archivo de texto con los términos y condiciones.
    - txt_aceptar: Texto del checkbox de aceptación.
    - sig_ruta: Ruta a la siguiente sección en caso de aceptación.

    Returns:
    - Tuple: Contiene la interfaz generada para la sección de términos y condiciones.
    """

    txt_titulo_terminos = ft.Text(titulo, size=18)
    terminos_condiciones = ft.Text(file.read(), size=14)
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

    btn_accept = ft.Checkbox(label=txt_aceptar, on_change=habilitar_next)
    btn_next = controles.next
    btn_next.current.on_click = lambda _: page.go(sig_ruta)

    return (
        ft.Row([ txt_titulo_terminos ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(contenido_term_cond, border=ft.border.all(1)),
        ft.Row([ btn_accept ])
    )

def config_instalacion(page, controles, varsInstal, titulo, text_seleccionar_carpeta, text_info, text_cambiar_ruta, text_expacio:str, sig_ruta:str) -> tuple:
    """
    Genera una interfaz para la sección de instalación.

    Parameters:
    - page: Página actual de la aplicación.
    - controles: Controles de la aplicación.
    - varsInstal: Variables relacionadas con la instalación.
    - titulo: Título de la sección de instalación.
    - text_seleccionar_carpeta: Texto para la selección de carpeta.
    - text_info: Información adicional.
    - text_cambiar_ruta: Texto para cambiar la ruta de instalación.
    - text_expacio: Texto que muestra el espacio disponible.
    - sig_ruta: Ruta a la siguiente sección.

    Returns:
    - Tuple: Contiene la interfaz generada para la sección de instalación.
    """

    if controles["install"]:
        controles.install.current.visible = False
    controles.next.current.visible = True
    controles.next.current.disabled = False
    controles.next.current.on_click = lambda _: page.go(sig_ruta)

    def select_file(e: ft.FilePickerResultEvent):
        filepicker.get_directory_path(text_seleccionar_carpeta)

    def return_path(e: ft.FilePickerResultEvent): 
        if not e.path: return
        varsInstal.path_instalacion = e.path
        directory_path.value = e.path
        directory_path.update()
    
    directory_path = ft.Text(value=varsInstal.path_instalacion, expand=1)
    filepicker = ft.FilePicker(on_result=return_path)
    
    controles.appbar.title= ft.Text(titulo)

    return (
        ft.Text(text_info, size=16),
        ft.Text(text_cambiar_ruta, size=14),
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
            ft.Text(text_expacio.format(helpers.get_format_size(varsInstal.path_instalador)), size=15),
        ])
    )

def config(page, controles, varsInstal, titulo, txt_btn_instalar:str, txt_checkbox_path, msg_agregar_path, variable_agregar_path, sig_ruta:str) -> tuple:
    """
    Genera una interfaz para la configuración antes de la instalación.

    Parameters:
    - page: Página actual de la aplicación.
    - controles: Controles de la aplicación.
    - varsInstal: Variables relacionadas con la instalación.
    - titulo: Título de la sección de configuración.
    - txt_btn_instalar: Texto del botón de instalación.
    - txt_checkbox_path: Texto del checkbox de agregar al PATH.
    - msg_agregar_path: Mensaje informativo sobre agregar al PATH.
    - variable_agregar_path: Variable que indica si agregar al PATH.
    - sig_ruta: Ruta a la siguiente sección.

    Returns:
    - Tuple: Contiene la interfaz generada para la sección de configuración.
    """
    controles.appbar.title = ft.Text(titulo)

    controles.agregar_boton(txt_btn_instalar.lower(), txt_btn_instalar, on_click=lambda _: page.go(sig_ruta))
    controles.next.current.visible = False

    def agregar_al_Path(e):
        if not agregar_path.value: return
        varsInstal[variable_agregar_path] = True
    
    agregar_path = ft.Checkbox(label=txt_checkbox_path, on_change=agregar_al_Path)
    return (
        ft.Text(msg_agregar_path, size=18),
        agregar_path
    )

def instalacion(page, controles, id_btn_back, id_btn_install, pbRef:ft.Ref[ft.ProgressBar], msg_progreso) -> None:
    """
    # IMPORTANTE
    Esta función no retorna una tupla
    La función de instalación debe ser implementada por usted

    ### Ejemplo:
    
    controles.cancel.current.visible = False
    regalo.instalar_regalo(pbRef.current, varsInstal.path_instalacion)
    controles.agregar_boton("fin", "Cerrar", on_click=lambda _: page.window_destroy())
    return (ft.Text("Instalación finalizada", size=18), ft.Text("El programa se ha instalado correctamente", size=14))
    """
    controles.eliminar_boton(id_btn_back)
    controles.eliminar_boton(id_btn_install)
    
    page.views.append(
        ft.View(
            page.route,
            [
                controles.appbarRef.current,
                ft.Column([ft.Text(msg_progreso, size=15), ft.ProgressBar(ref=pbRef, width=500)]),
            ]
        )
    )
    controles.cancel.current.visible = False
    page.update()

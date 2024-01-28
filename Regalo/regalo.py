import flet as ft
from pathlib import Path
from typing import Callable, Union

from .helpers.install_helpers import copiar_exe, agregar_al_Path
from .components import Modal_Cerrar, Controles
from .pages import Paginas
from .vars import InstallerVars

class Regalo():
    def __init__(self, nombre_regalo:str, path_instalador_exe:str, paginas:Paginas, vars_config:dict={}, args_modal_cerrar:dict=None, func_config:Callable=None, mostrar_siempre_appbar:bool=False):
        self.pages:Paginas = paginas
        self.__page:ft.Page = None

        self.path_instalador_exe:Path = Path(path_instalador_exe)
        if not self.path_instalador_exe.exists():
            raise FileNotFoundError(f"El archivo {self.path_instalador_exe} no existe")
        
        self.nombre_regalo = nombre_regalo

        self.kwargs_app_flet = None
        self.mostrar_siempre_appbar = mostrar_siempre_appbar
        self.func_config = func_config
        self.variables_instalador = InstallerVars(vars_config)
        self.variables_instalador["path_instalador"] = path_instalador_exe

        # Componentes de dialog para cerrar
        self.args_modal_cerrar = args_modal_cerrar or {
            "titulo": "En serio?",
            "contenido": "Quieres cancelar la instalación?",
            "txt_accept": "Yep",
            "txt_cancel": "No ._.",
        }
        self.confirm_dialog = Modal_Cerrar(**self.args_modal_cerrar)

        self.controles_inst:Controles = Controles()

    def handler_cerrar_instalador(self) -> ft.AlertDialog:
        return self.confirm_dialog.crear(self.__page)
    
    def abrir(self, main, **kwargs):
        self.kwargs_app_flet = kwargs
        self.main = main
        ft.app(target=self.app, view=ft.AppView.FLET_APP)
    
    def instalar_regalo(self, pb:ft.ProgressBar, path_instalacion) -> Union[None, tuple[bool, str]]:
        path_instalacion = Path(path_instalacion)
        if path_instalacion.name.lower() != self.nombre_regalo.lower():
            path_instalacion = path_instalacion / self.nombre_regalo
        
        if path_instalacion.exists():
            path_instalacion.rmdir()
        path_instalacion.mkdir(parents=True, exist_ok=True)  
        
        ext = self.path_instalador_exe.suffix
        filename = f"{self.path_instalador_exe.stem}{ext}"

        pb.value = 0
        for porcentaje in copiar_exe(self.path_instalador_exe, path_instalacion / filename):
            pb.value = porcentaje

        if self.variables_instalador.get("agregar_path"):
            return agregar_al_Path(path_instalacion)

    def __route_change(self, event:ft.RouteChangeEvent):
        ruta = event.route

        pagina = self.pages.get(ruta)
        if not pagina: return
        self.render(ruta, pagina)

    def __llamar_view(self, func):
        return func(self.__page, self.controles_inst, self.variables_instalador)

    def __view_pop(self, event):
        self.__page.views.pop()
        top_view = self.__page.views.pop()
        self.__page.go(top_view.route)

    def render(self, ruta, pagina):
        self.controles_inst.appbar.title = pagina.titulo
        contenido = self.__llamar_view(pagina.pag)
        appBar = self.controles_inst.appbar
        appBar.title = pagina.titulo if appBar.title == "" and pagina.titulo else appBar.title

        render = [
            appBar,
            ft.Container(content=ft.Column(contenido), expand=True),
            self.controles_inst.render(alignment=ft.MainAxisAlignment.END)
        ]
        
        if not self.mostrar_siempre_appbar and ruta == "/": render.pop(0)

        if contenido:
            self.__page.views.append(ft.View(ruta, render))
        self.__page.update()

    def inicial_config(self, page):    
        for k,v in self.kwargs_app_flet.items():
            setattr(page, k, v)
            
        page.on_route_change = self.__route_change
        page.on_view_pop = self.__view_pop
        
        confirm_dialog = self.handler_cerrar_instalador()

        def window_event(e):
            if e.data == "close" or not e.data:
                page.dialog = confirm_dialog
                confirm_dialog.open = True
                page.update()

        self.controles_inst.agregar_boton("next", "Next")
        self.controles_inst.agregar_boton("cancel", "Cancel", on_click=window_event)
        self.controles_inst.agregar_pb("pb")

    def app(self, page: ft.Page):
        self.pages.agregar("/", self.main)
        self.__page = page
        self.inicial_config(self.__page)
        if self.func_config: self.func_config(self.__page, self.controles_inst, self.variables_instalador)

        page.views.clear()
        self.render("/", self.pages.get("/"))
        
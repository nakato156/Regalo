import flet as ft

class Modal_Cerrar:
    def __init__(self,  titulo, contenido, txt_accept, txt_cancel):
        self.__page = None
        self.titulo = titulo
        self.contenido = contenido
        self.titulo = titulo
        self.btn_accept = txt_accept
        self.btn_cancel = txt_cancel
    
    def crear(self, page) -> ft.AlertDialog:
        self.__page = page
        def yes_click(e):
            self.__page.window_destroy()

        def no_click(e):
            confirm_dialog.open = False
            self.__page.update()
            
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(self.titulo),
            content=ft.Text(self.contenido),
            actions=[
                ft.ElevatedButton(self.btn_accept, on_click=yes_click),
                ft.OutlinedButton(self.btn_cancel, on_click=no_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return confirm_dialog
import flet as ft
from typing import Tuple, Any

class Controles:
    def __init__(self) -> None:
        valType = Tuple[ft.Ref[ft.TextField], ft.ElevatedButton, tuple]
        
        self.botones: dict[str, valType] = {}
        self.controles: dict[str, Any] = {}

        self.appbarRef:ft.Ref[ft.AppBar] = ft.Ref[ft.AppBar]()
        self.appbar:ft.AppBar = ft.AppBar(ref=self.appbarRef)

    def __getitem__(self, item):
        if item in self.botones.keys():
            return self.botones[item][1]
        elif item in self.controles.keys():
            return self.controles[item][1]

    def get_btn(self, id: str) -> ft.Ref[ft.ElevatedButton]:
        return self.botones[id][1]
    
    def get_control(self, id: str) -> ft.Ref[Any]:
        return self[id]
    
    def __getattr__(self, name: str) -> ft.Ref[ft.ElevatedButton]:
        if name in self.botones.keys():
            return self.botones[name][0]
        elif name in self.controles.keys():
            return self.controles[name][0]
        return super().__getattribute__(name)

    def agregar_boton(self, id, texto, **kwargs:dict):
        ref_btn = ft.Ref[ft.ElevatedButton]()
        btn = ft.ElevatedButton(texto, ref=ref_btn, **kwargs)
        self.botones[id] = (ref_btn, btn, tuple(kwargs.items()))
        return btn

    def agregar_pb(self, id, **kwargs):
        ref_pb = ft.Ref[ft.ProgressBar]()
        pb = ft.ProgressBar(ref=ref_pb )
        self.controles[id] = (ref_pb, pb)
        return pb
    
    def eliminar_control(self, id):
        if id in self.botones.keys(): del self.botones[id]
        if id in self.controles.keys(): del self.controles[id]

    def reset(self):
        for ref, btn, args in self.botones.values():
            for name, val in args:
                setattr(btn, name, val)
            ref.current.update()

    def render(self, **kwargs) -> ft.Row:
        return ft.Row([btn[1] for btn in self.botones.values()], **kwargs)
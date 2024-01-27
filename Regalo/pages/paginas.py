from typing import Callable, Any, Union
from ..components import Controles
import flet as ft

class Pagina:
    def __init__(self, func:Callable[[ft.Page, Controles, Any], tuple], titulo:str="") -> None:
        self.pag = func
        self.titulo = titulo

class Paginas:
    def __init__(self, pags:dict[str, Union[Callable, Pagina]]={}):
        self.paginas:dict = {}
        for k, pag in pags.items():
            self.agregar(k, pag)
    
    def get_titulo_pag(self, id) -> Union[str, None]:
        pag = self.paginas.get(id, None)
        if pag:
            return pag[1] if isinstance(pag, (tuple, list)) and len(pag) > 1 else ""
        return None

    def agregar(self, ruta:str, pag:Union[Callable[[ft.Page, Controles, Any], tuple], Pagina]):
        pagina = pag if isinstance(pag, Pagina) else Pagina(pag, "")
        self.paginas[ruta] = pagina
    
    def get(self, ruta:str) -> Union[Pagina, None]:
        return self.paginas.get(ruta, None)
    
    def __len__(self):
        return len(self.paginas)


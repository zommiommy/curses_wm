
from typing import Union, Dict

from .window import Window

class BoxSubWindow():
    """Wrapper class over all the data associated to a window in a DinamicBox."""
    def __init__(self,win : Window, **kwargs):
        self.window = win
        self.weight : int = kwargs.get("weight",1)
        self.priority : int = kwargs.get("priority",1)

        self.display : bool = True
        self.actual_dim : int = 0

        self.min_dimension : Dict[str,Union[float,int]] =  kwargs.get("min_dimension",win.get_default_min_dim())
        if self.min_dimension["y"] < 0:
            self.min_dimension["y"] = 0
        if self.min_dimension["x"] < 0:
            self.min_dimension["x"] = 0

        self.max_dimension : Dict[str,Union[float,int]] =  kwargs.get("max_dimension",win.get_default_max_dim())
        if self.max_dimension["y"] < 0:
            self.max_dimension["y"] = 0
        if self.max_dimension["x"] < 0:
            self.max_dimension["x"] = 0
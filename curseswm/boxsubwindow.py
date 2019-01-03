
from .window import Window

class BoxSubWindow():
    """Wrapper class over all the data associated to a window in a DinamicBox."""
    def __init__(self,win : Window, **kwargs):
        self.window = win
        self.weight : int = kwargs.get("weight",1)
        self.priority : int = kwargs.get("priority",1)

        self.display : bool = True
        self.actual_dim : int = 0

        self.min_dimension : int =  kwargs.get("min_dimension",win.get_default_min_dim())
        if self.min_dimension < 0:
            self.min_dimension = 0

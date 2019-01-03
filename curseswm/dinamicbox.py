
from typing import List

from .window import Window
from .horribleworkaround import horrible_workaround

class DynamicBox():
    """Class that abstract the common features of the HBox and the VBox"""

    def __init__(self):
        """Initialize an empty DynamicBox."""
        self.window_list = []
        self.weight_list   : List[int]  = []
        self.priority_list : List[int]  = []
        self.display_list  : List[bool] = []
    
    def _start(self) -> None:
        """Initialize all the subclasses"""
        [win._start() for win in self.window_list]

    def _refresh(self) -> None:
        """Refresh all the sub windows"""
        [win._refresh() for win in self.window_list]
        
    def _erase(self) -> None:
        """Erase all the sub windows"""
        [win._erase() for win  in self.window_list]

    def add_window(self, win: Window, weight: int = 1, priority : int = 1, min_dim : int = 1) -> None:
        """Add a window to the DynamicBox"""
        self.window_list.append(win)
        self.weight_list.append(weight)
        self.priority_list.append(priority)
        self.display_list.append(True)

    def _normalize_weights(self, max_dim : int) -> List[int]:
        """Return the list of the dimension of all the windows based on the weights"""
        weight_total = sum(self.weight_list, 0)
        weights = list(map(lambda x: int(max_dim * x / weight_total),self.weight_list))
        # correct the rounding errors giving the columns left to the first window
        weights[0] += (max_dim - sum(weights, 0))
        return weights

    def _resize_routine(self, new_x : int = 0, new_y : int = 0) -> None:
        """Method that the Hbox and VBox are supposed to overwrite."""
        raise NotImplementedError

    def resize(self, width : int, height : int) -> None:
        """Resize method if the class is a child."""
        # Update to the new dimension
        self.height, self.width = height, width
        self._resize_routine()

    def _move_window(self, new_x : int, new_y : int) -> None:
        """Move the windows so that the upper left corner is at new_x and new_y"""
        self._resize_routine(new_x, new_y)



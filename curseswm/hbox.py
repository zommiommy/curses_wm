
from typing import Union


from .window import Window
from .dinamicbox import DynamicBox
from .boxsubwindow import BoxSubWindow

class HBox(DynamicBox):
    """Class to put multiple windows on weighted columns on the same row."""

    def get_win_min_dim(self, win : BoxSubWindow) -> Union[int,float]:
        """Return the min dimension of the windows that the V or H box are intrested in."""
        return win.min_dimension["x"]
        
    def get_win_max_dim(self, win : BoxSubWindow) -> Union[int,float]:
        """Return the max dimension of the windows that the V or H box are intrested in."""
        return win.max_dimension["x"]

    def _resize_routine(self, new_x = 0, new_y = 0):
        # Normalize the weights
        self._find_fitting(self.width)
        # update the sub windows dimension and move them
        x = new_x
        for obj in self.window_list:
            if obj.display:
                obj.window.resize(obj.actual_dim, self.height)
                obj.window._move_window(x,new_y)
                x += obj.actual_dim
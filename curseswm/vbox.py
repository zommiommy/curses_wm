

from typing import Union


from .window import Window
from .dinamicbox import DynamicBox
from .boxsubwindow import BoxSubWindow

class VBox(DynamicBox):
    """Class to put multiple windows on weighted rows on the same columns."""

    def get_win_min_dim(self, win : BoxSubWindow) -> Union[int,float]:
        """Return the min dimension of the windows that the V or H box are intrested in."""
        return win.min_dimension["y"]
        
    def get_win_max_dim(self, win : BoxSubWindow) -> Union[int,float]:
        """Return the max dimension of the windows that the V or H box are intrested in."""
        return win.max_dimension["y"]

    def _resize_routine(self, new_x = 0, new_y = 0):
        # Normalize the weights
        self._find_fitting(self.height)
        # update the sub windows dimension and move them
        y = new_y
        for obj in self.window_list:
            if obj.display:
                obj.window.resize(self.width, obj.actual_dim)
                obj.window._move_window(new_x, y)
                y += obj.actual_dim

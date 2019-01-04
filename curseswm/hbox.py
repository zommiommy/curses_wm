
from .window import Window
from .dinamicbox import DynamicBox

class HBox(DynamicBox):
    """Class to put multiple windows on weighted columns on the same row."""
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
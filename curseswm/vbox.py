

from .window import Window
from .dinamicbox import DynamicBox

class VBox(DynamicBox):
    """Class to put multiple windows on weighted rows on the same columns."""
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

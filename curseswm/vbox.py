

from .window import Window
from .dinamicbox import DynamicBox

class VBox(DynamicBox):
    """Class to put multiple windows on weighted rows on the same columns."""
    def _resize_routine(self, new_x = 0, new_y = 0):
        # Normalize the weights
        win_dimensions = self._normalize_weights(self.height)
        # update the sub windows dimension and move them
        y = new_y
        for win, dimension, display in zip(self.window_list, win_dimensions, self.display_list):
            if display:
                win.resize(self.width, dimension)
                win._move_window(new_x, y)
                y += dimension
            else:
                win.resize(0,0)
                win._move_window(0,0)

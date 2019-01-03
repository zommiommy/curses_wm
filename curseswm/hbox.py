
from .window import Window
from .dinamicbox import DynamicBox

class HBox(DynamicBox):
    """Class to put multiple windows on weighted columns on the same row."""
    def _resize_routine(self, new_x = 0, new_y = 0):
        # Normalize the weights
        win_dimensions = self._normalize_weights(self.width)
        # update the sub windows dimension and move them
        x = new_x
        for win, dimension, display in zip(self.window_list, win_dimensions, self.display_list):
            if display:
                win.resize(dimension, self.height)
                win._move_window(x,new_y)
                x += dimension
            else:
                win.resize(0,0)
                win._move_window(0,0)
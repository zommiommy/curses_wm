
from wrapt import synchronized

from curseswm.window import Window

class VBox():
    """Class to put multiple windows on weighted rows on the same columns."""

    def __init__(self):
        """Initialize an empyt HBox."""
        self.window_list = []
        self.weight_list = []
    
    def _start(self):
        """Initialize all the subclasses"""
        [win._start() for win in self.window_list]

    def add_window(self, win: Window, weight: int = 1):
        """Add a window to the Hbox"""
        self.window_list.append(win)
        self.weight_list.append(weight)

    @synchronized
    def _refresh(self):
        """Refresh all the sub windows"""
        [win._refresh() for win  in self.window_list]

    def _resize_routine(self, new_x = 0, new_y = 0):
        # Normalize the weights
        weight_total = sum(self.weight_list, 0)
        weights = list(map(lambda x: int(self.height * x / weight_total),self.weight_list))
        # Correct rounding errors by increasing the first window
        weights[0] += (self.height - sum(weights, 0))
        # update the sub windows dimension and move them
        y = new_y
        for win, weight in zip(self.window_list, weights):
            win.resize(self.width, weight)
            win._move_window(new_x, y)
            y += weight


    def resize(self, width, height):
        """Resize method if the class is a child."""
        # Update to the new dimension
        self.height, self.width = height, width
        self._resize_routine()

    def _move_window(self, new_x, new_y):
        """Move the windows so that the upper left corner is at new_x and new_y"""
        self._resize_routine(new_x, new_y)

    def _erase(self):
        """Erase all the sub windows"""
        [win._erase() for win  in self.window_list]


from window import Window
from wrapt import synchronized

class HBox():
    """Class to put multiple windows on weighted columns on the same row."""

    def __init__(self):
        """Initialize an empyt HBox."""
        self.window_list = []
        self.weight_list = []
        self._is_displayed = False
    
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
        if self.is_displayed():
            [win._refresh() for win  in self.window_list]

    def _resize_routine(self, new_x = 0, new_y = 0):
        # Normalize the weights
        weight_total = sum(self.weight_list, 0)
        weights = list(map(lambda x: int(self.width * x / weight_total),self.weight_list))

        weights[0] += (self.width - sum(weights, 0))
        # update the sub windows dimension and move them
        x = new_x
        for win, weight in zip(self.window_list, weights):
            win.resize(weight, self.height)
            win._move_window(x,new_y)
            x += weight

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

    def set_displayed(self, value: bool):
        self._is_displayed = value
        [win.set_displayed(value) for win  in self.window_list]
    
    def is_displayed(self):
        return self._is_displayed

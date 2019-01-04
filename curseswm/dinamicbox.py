
from typing import List

from .window import Window
from .boxsubwindow import BoxSubWindow
from .horribleworkaround import horrible_workaround

class DynamicBox():
    """Class that abstract the common features of the HBox and the VBox"""

    def __init__(self):
        """Initialize an empty DynamicBox."""
        self.window_list = []
    
    def _start(self) -> None:
        """Initialize all the subclasses"""
        [win.window._start() for win in self.window_list]

    def _refresh(self) -> None:
        """Refresh all the sub windows"""
        [win.window._refresh() for win in self.window_list if win.display]
        
    def _erase(self) -> None:
        """Erase all the sub windows"""
        [win.window._erase() for win in self.window_list]

    def add_window(self, win: Window, **kwargs) -> None:
        """Add a window to the DynamicBox.
        add_window( win : Window,
                    weight : int = 1,
                    priority : int = 1,
                    min_dimension : int = 0)"""
        self.window_list.append(BoxSubWindow(win, **kwargs))

    def _reset_display_of_windows(self) -> None:
        """Reset all the windows to display True so the solution start clean"""
        for obj in self.window_list:
            obj.display = True

    def _get_weights_list(self) -> List[int]:
        """Return the list of the """
        return list(map(lambda x: x.weight, filter(lambda x: x.display, self.window_list)))
    def _get_total_weights(self) -> int:
        """Return the sum of all the weights"""
        return sum(self._get_weights_list(), 0)

    def _calculate_dimensions(self, max_dim : int) -> None:
        """Return the list of the dimension of all the windows based on the weights"""
        weight_total = self._get_total_weights()

        total_dim : int = 0
        for obj in self.window_list:
            if obj.display:
                obj.actual_dim = int(max_dim * obj.weight / weight_total)
                total_dim += obj.actual_dim
            else:
                obj.actual_dim = 0

        # correct the rounding errors giving the columns left to the first window
        first_obj = [x for x in self.window_list if x.display][0]
        first_obj.actual_dim += (max_dim - total_dim)

    def _solution_is_not_feasable(self)-> None:
        for obj in self.window_list:
            if obj.display and obj.actual_dim > obj.min_dimension:
                return False
        return True

    def _shutoff_lowest_priority(self)-> None:
        """Set the window with the lowest priority display attribute to false """
        lowest = min(self.window_list, key=lambda x: x.priority)
        lowest.display = False

    def _find_fitting(self, max_dim : int) -> None:
        # Reset the solution
        self._reset_display_of_windows()
        # Calculate an initial solution
        self._calculate_dimensions(max_dim)
        # While the solution is not feasable
        while self._solution_is_not_feasable():
            # Remove the lowest priority
            self._shutoff_lowest_priority()
            # Recalc the solution
            self._calculate_dimensions(max_dim)


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

    def get_default_min_dim(self) -> int:
        """return the minimum dimension of a dynamic box."""
        return 0   
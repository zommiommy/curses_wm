
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
        [win.window._refresh() for win in self.window_list if win.display ]
        
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
        """Return the list of the weights"""
        return [x.weight for x in self.window_list if x.display]

    def _get_total_weights(self) -> int:
        """Return the sum of all the weights"""
        return sum(self._get_weights_list(), 0)

    def _get_actual_dim_list(self) -> List[int]:
        """Return the list of the actual_dims"""
        return [x.actual_dim for x in self.window_list if x.display]

    def _find_first_displayed_window(self) -> BoxSubWindow:
        """Return the first window in list with display = True"""
        try:
            return next((x for x in self.window_list if x.display))
        except StopIteration:
            return None

    def _get_total_actual_dim(self) -> int:
        """Return the sum of all the actual_dim of all the windows in list with display set to True"""
        return sum(self._get_actual_dim_list(),0)

    def _correct_dimensions(self, max_dim : int) -> None:
        """correct the rounding errors giving the columns left to the first window"""
        current_dim = self._get_total_actual_dim()
        first_obj = self._find_first_displayed_window()
        if first_obj:
            # Add the error to the first window
            first_obj.actual_dim += (max_dim - current_dim)

    def _calculate_dimensions(self, max_dim : int) -> None:
        """Return the list of the dimension of all the windows based on the weights"""
        weight_total = self._get_total_weights()

        for obj in self.window_list:
            if obj.display:
                obj.actual_dim = int(max_dim * obj.weight / weight_total)
            else:
                obj.actual_dim = 1

        self._correct_dimensions(max_dim)

    def _solution_is_feasable(self)-> None:
        """Check if all the displayed window have the actual dim bigger or equal than their min dimension."""
        # Original statement
        # all(display => actual_dim >= min_dim)
        # Derivation of a faster one (the solution will be unfeasible most of the time so any is better than all)
        # not any( not (display => actual_dim >= min_dim))
        # not any( not (not display or actual_dim >= min_dim))
        # not any(display and not actual_dim >= min_dim))
        # not any(display and actual_dim < min_dim))
        gen = (obj.display and obj.actual_dim < obj.min_dimension for obj in self.window_list)
        return not any(gen)

    def _shutoff_lowest_priority(self)-> None:
        """Set the window with the lowest priority display attribute to false """
        lowest = min((win for win in self.window_list if win.display), key=lambda x: x.priority)
        lowest.display = False

    def _find_fitting(self, max_dim : int) -> None:
        # Reset the solution
        self._reset_display_of_windows()
        # Calculate an initial solution
        self._calculate_dimensions(max_dim)
        # While the solution is not feasable
        while not self._solution_is_feasable():
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
        return 1 
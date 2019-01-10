
from typing import List, Union, Dict

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
                    min_dimension : int = win.get_default_min_dim())"""
        self.window_list.append(BoxSubWindow(win, **kwargs))

    def _reset_display_of_windows(self) -> None:
        """Reset all the windows to display True so the solution start clean"""
        for obj in self.window_list:
            obj.display = True

    def _reset_actual_dim_of_windows(self) -> None:
        """Reset all the windows assigned dimensions."""
        for obj in self.window_list:
            obj.actual_dim = 0

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
            # return the first window that is displayed and that have the actual_dim not set to the max dim so that in the case
            # of all windows setted with the max this will return None and the _correct_dimensions will not trigger
            # else it will get into an endless loop of correcting the dim and resetting it to the max.
            return next((x for x in self.window_list if x.display and x.actual_dim != self.get_win_max_dim(x)))
        except StopIteration:
            return None

    def _get_total_actual_dim(self) -> int:
        """Return the sum of all the actual_dim of all the windows in list with display set to True"""
        return sum(self._get_actual_dim_list(),0)

    def _correct_dimensions(self, max_dim : int) -> None:
        """correct the rounding errors giving the columns left to the first window"""
        current_dim = self._get_total_actual_dim()
        first_obj = self._find_first_displayed_window()
        if first_obj and max_dim >= current_dim:
            # Add the error to the first window
            first_obj.actual_dim += (max_dim - current_dim)

    def _calculate_dimensions(self, max_dim : int) -> None:
        """Return the list of the dimension of all the windows based on the weights"""
        # Get all the windows left to be assigned
        free_objs = [x for x in self.window_list if x.display and x.actual_dim == 0]
        # Get the weights of the windows left to be assigned
        weight_total = sum((x.weight for x in free_objs),0)
        # Remove the space for the already settled windows from the assignable space
        max_dim = max_dim - sum((x.actual_dim for x in self.window_list),0)

        for obj in self.window_list:
            if obj.display and obj.actual_dim == 0:
                obj.actual_dim = int(max_dim * obj.weight / weight_total)

        self._correct_dimensions(max_dim)

    def _max_casting_routine(self):
        """Clip to the max the windows that violate the max constraint and reset the correct ones."""
        for x in self.window_list:
            # If the window violates his constraint or it's have already been setted to the max, set it to the max.
            if x.actual_dim >= self.get_win_max_dim(x):
                x.actual_dim = self.get_win_max_dim(x)
            else:
                # Else reset it to 0 so that at the next iteration can be assigned
                x.actual_dim = 0

    def _find_max_fitting(self, max_dim : int) -> None:
        """Find a fitting so that all the max constraint are respected"""
        # Calculate a solution
        self._reset_actual_dim_of_windows()
        self._calculate_dimensions(max_dim)
        # While it's not feasible then cast to the max the windows that don't satisfies
        #  the constraints and try to recalculate the solution.
        while not self._solution_is_max_feasible() or not self._solution_is_inside_bounds(max_dim):
            # If the values are at max and their sums is bigger than the max_dim then shutoff a window
            if not self._solution_is_inside_bounds(max_dim):
                self._shutoff_lowest_priority()
            # Cast to the max if some window violate the max constraint
            self._max_casting_routine()
            # with those new informations try to find a new solutions
            self._calculate_dimensions(max_dim)

    def _solution_is_inside_bounds(self, max_dim):
        """Return if the total sum of the actual dim of the windows is less than the max_dim or else."""
        return self._get_total_actual_dim() <= max_dim

    def _solution_is_min_feasible(self)-> None:
        """Check if all the displayed window have the actual dim bigger or equal than their min dimension."""
        # Original statement
        # all(display => actual_dim >= min_dim)
        # Derivation of a faster one (the solution will be unfeasible most of the time so any is better than all)
        # not any( not (display => actual_dim >= min_dim))
        # not any( not (not display or actual_dim >= min_dim))
        # not any(display and not actual_dim >= min_dim))
        # not any(display and actual_dim < min_dim))
        gen = (obj.display and obj.actual_dim < self.get_win_min_dim(obj) for obj in self.window_list)
        return not any(gen)

    def _solution_is_max_feasible(self)-> None:
        """Check if all the displayed window have the actual dim bigger or equal than their min dimension."""
        # For the derivation look at the min feasible
        gen = (obj.display and obj.actual_dim > self.get_win_max_dim(obj) for obj in self.window_list)
        return not any(gen)

    def _shutoff_lowest_priority(self)-> None:
        """Set the window with the lowest priority display attribute to false """
        lowest = min((win for win in self.window_list if win.display), key=lambda x: x.priority)
        lowest.display = False

    def _find_fitting(self, max_dim : int) -> None:
        """Find an assignment of dimension so that all the min and max constraint are satisfied.
        This is a generalized weighted knapsack with priority and can be formulated as a shortest path problem but
        the simplex or Dijkstra seems to computationally heavy to resolve in real time so a max-min greedy approach was chosen.
        This algorithm start with all the window displayed than find a solution that satisfies the max constraint and then
        check if the solution satisfies the min constraints. this has complexity O(w^2) where w is the number of windows."""
        # Reset the solution
        self._reset_display_of_windows()
        # Calculate an initial solution
        self._find_max_fitting(max_dim)
        # While the solution is not feasible
        while not self._solution_is_min_feasible():
            # Remove the lowest priority
            self._shutoff_lowest_priority()
            # Recalc the solution
            self._find_max_fitting(max_dim)


    def _resize_routine(self, new_x : int = 0, new_y : int = 0) -> None:
        """Method that the Hbox and VBox are supposed to overwrite."""
        raise NotImplementedError

    def get_win_min_dim(self, win : Window) -> Union[int,float]:
        """Return the min dimension of the windows that the V or H box are intrested in."""
        raise NotImplementedError
        
    def get_win_max_dim(self, win : Window) -> Union[int,float]:
        """Return the max dimension of the windows that the V or H box are intrested in."""
        raise NotImplementedError

    def resize(self, width : int, height : int) -> None:
        """Resize method if the class is a child."""
        # Update to the new dimension
        self.height, self.width = height, width
        self._resize_routine()

    def _move_window(self, new_x : int, new_y : int) -> None:
        """Move the windows so that the upper left corner is at new_x and new_y"""
        self._resize_routine(new_x, new_y)

    def get_default_min_dim(self) -> Dict[str,Union[float,int]]:
        """return the minimum dimension of a dynamic box."""
        objs = [x.window.get_default_min_dim() for x in self.window_list]
        return {"x":min([x["x"] for x in objs]),"y":min([x["y"] for x in objs])}

    def get_default_max_dim(self) -> Dict[str,Union[float,int]]:
        """return the minimum dimension of a dynamic box."""
        objs = [x.window.get_default_max_dim() for x in self.window_list]
        return {"x":sum([x["x"] for x in objs],0),"y":sum([x["y"] for x in objs],0)}
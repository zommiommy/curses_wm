
import curses
from typing import Tuple
from wrapt import synchronized

from curseswm.colours import TextColour, BorderColour
from .offsettable import offsettable_row, offsettable_col

class Window():
    """Base class to display a window. This class is ment to be extendend
     by subclasses which will have to override the _refresh method to draw
     its content on the screen at each refresh and it can draw using the 
     draw_text and insert_character methods."""

    def __init__(self,title:str = "", **kwargs):
        """Initialize the Window."""
        self.set_title(title)
        self.win = None
        self.width : int = 0
        self.height : int = 0
        self.display_border : bool = kwargs.get("display_border",True)

    def _check_x(self, x: int) -> bool:
        """Check if the given x is inside the window or else."""
        return x > self.get_last_col() or x < self.get_first_col()

    def _check_y(self, y: int) -> bool:
        """Check if the given y is inside the window or else."""
        return  y > self.get_last_row() or y < self.get_first_row()

    def _check_bounds(self, x: int, y: int) -> bool:
        """Check if the given coordinates are inside the window or else."""
        return self._check_x(x) or self._check_y(y)

    def _get_writtable_window(self, x: int) -> int:
        """Return how many characters are writtable starting from x until the bound"""
        return (self.get_last_col() + 1) - x   

    def draw_text(self, x : int, y : int, string : str) -> bool:
        """Display a text on the windows, respecting the window dimensions.
        Return if the drawn was sucessfully inside the window or else."""
        # Check if the text is in the bound of the window
        if self._check_bounds(x,y) :
            return False

        writtable_window = self._get_writtable_window(x)

        #for line in string.split("\n"):
        #    y += 1
        #    if y > self.get_last_row():
        #        return False
        self.win.addnstr(y, x, string, writtable_window)
        # This line would do the same but for some reason
        # It messes up the corner of all the windows
        # self.win.insstr(y + 1, x + 1, string)
        return True

    def get_shape(self) -> Tuple[int,int]:
        """Return the current dimension of the window as (width, height)."""
        return (self.width, self.height)

    def clip_to_bounds_x(self, x: int) -> int:
        """Helper method to clip the coordinate to the nearest feasiable ones."""
        if x < self.get_first_col():
            x = self.get_first_col()
        elif x > self.get_last_col():
            x = self.get_last_col()
        return x

    def clip_to_bounds_y(self, y: int) -> int:
        """Helper method to clip the coordinate to the nearest feasiable ones."""
        if y < self.get_first_col():
            y = self.get_first_col()
        elif y > self.get_last_col():
            y = self.get_last_col()
        return y

    def clip_to_bounds(self, x : int, y : int) -> Tuple[int, int]:
        """Helper method to clip the coordinate to the nearest feasiable ones."""
        return (self.clip_to_bounds_x(x), self.clip_to_bounds_y(y))


    @offsettable_row
    def get_first_row(self) -> int:
        """Return the index to write on the first line of the window."""
        if self.display_border:
            return 1
        return 0

    @offsettable_row
    def get_mid_row(self) -> int:
        """Return the index of the middle row"""
        return int((self.get_last_row() - self.get_first_row()) / 2) 

    @offsettable_row
    def get_last_row(self) -> int:
        """Return the index to write on the last line of the window."""
        if self.display_border:
            return self.height - 2
        return self.height - 1

    @offsettable_col
    def get_first_col(self) -> int:
        """Return the index to write on the first col of the window."""
        if self.display_border:
            return 1
        return 0

    @offsettable_col
    def get_mid_col(self) -> int:
        """Return the index of the middle col"""
        return int((self.get_last_col() - self.get_first_col()) / 2) 

    @offsettable_col
    def get_last_col(self) -> int:
        """Return the index to write on the last line of the window."""
        if self.display_border:
            return self.width - 2
        return self.width - 1

    def _start(self) -> None:
        """Create the window, set it up, clean it and draw the result."""
        self.win = curses.newwin(1,1, 0, 0)
        self.win.keypad(1)
        self.win.clear()

    def get_title(self) -> str:
        """Get the title of the window."""
        return self.title

    def set_title(self,new_title : str) -> None:
        """Set the new title of the window."""
        self.title = " " + new_title.strip() + " "

    def _move_window(self, new_x : int, new_y : int) -> None:
        """Move the windows so that the upper left corner is at new_x and new_y"""
        self.win.mvwin(new_y, new_x)

    def _draw_border(self) -> None:
        """Draw borders around the window."""
        with BorderColour(self.win):
            self.win.border(0,0,0,0,0,0,0,0)

    def _draw_title(self) -> None:
        """Draw ther title on the top of the window."""
        if self.width > 1:
            self.win.addnstr(0, 1, self.title, self.width - 1)

    def _refresh(self) -> None:
        """Method to be overwritten by the subclasses to add the content."""
        self._refresh_iter()

    @synchronized
    def _refresh_iter(self) -> None:
        """Method to redraw the window."""
        if self.win:
            if self.display_border:
                self._draw_border()
                self._draw_title()
            self.win.refresh()

    def _erase(self) -> None:
        """Cancel all the window."""
        if self.win:
            self.win.erase()

    def resize(self, width : int, height : int) -> None:
        """Resize using fixed width and height."""
        self.height, self.width = height, width
        self.win.resize(self.height, self.width)
        self._refresh()



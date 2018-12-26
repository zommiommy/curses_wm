
import curses
from wrapt import synchronized
from colours import TextColour, BorderColour

class Window():
    """Base class to display a window. This class is ment to be extendend
     by subclasses which will have to override the _refresh method to draw
     its content on the screen at each refresh and it can draw using the 
     draw_text and insert_character methods."""

    def __init__(self,title:str = ""):
        """Initialize the Window."""
        self.set_title(title)
        self.win = None
        self.width = 0
        self.height = 0
        self._is_displayed = False

    def draw_text(self, x : int, y : int, string : str) -> bool:
        """Display a text on the windows, respecting the window dimensions.
        Return if the drawn was sucessfully inside the window or else."""
        # Check if the text is in the bound of the window
        error = x > (self.get_last_col() + 1)
        error |= x < self.get_first_col()
        error |= y > self.get_last_row()
        error |= y < self.get_first_row()
        if error :
            return False

        writtable_window = (self.get_last_col() + 1) - x - 2

        #for line in string.split("\n"):
        #    y += 1
        #    if y > self.get_last_row():
        #        return False
        self.win.addnstr(y, x, string, writtable_window)
        # This line would do the same but for some reason
        # It messes up the corner of all the windows
        # self.win.insstr(y + 1, x + 1, string)
        return True

    def get_shape(self):
        """Return the current dimension of the window as (width, height)."""
        return (self.width, self.height)

    def get_first_row(self):
        """Return the index to write on the first line of the window."""
        return 1

    def get_mid_row(self):
        """Return the index of the middle row"""
        return int(self.get_last_row() / 2)

    def get_last_row(self):
        """Return the index to write on the last line of the window."""
        # exlude the first
        return self.height - 2

    def get_first_col(self):
        """Return the index to write on the first col of the window."""
        return 1

    def get_mid_col(self):
        """Return the index of the middle col"""
        return int(self.get_last_col() / 2)

    def get_last_col(self):
        """Return the index to write on the last line of the window."""
        return self.width - 2

    def _start(self):
        """Create the window, set it up, clean it and draw the result."""
        self.win = curses.newwin(1,1, 0, 0)
        #self.win.nodelay(True)
        self.win.keypad(1)
        self.win.clear()

    def get_title(self):
        """Get the title of the window."""
        return self.title

    def set_title(self,new_title : str):
        """Set the new title of the window."""
        self.title = " " + new_title.strip() + " "

    def _move_window(self, new_x, new_y):
        """Move the windows so that the upper left corner is at new_x and new_y"""
        self.win.mvwin(new_y, new_x)

    def _draw_border(self):
        """Draw borders around the window."""
        with BorderColour(self.win):
            self.win.border(0,0,0,0,0,0,0,0)

    def _draw_title(self):
        """Draw ther title on the top of the window."""
        if self.width > 1:
            self.win.addnstr(0, 1, self.title, self.width - 1)

    def _refresh(self):
        """Method to be overwritten by the subclasses to add the content."""
        self._refresh_iter()

    @synchronized
    def _refresh_iter(self):
        """Method to redraw the window."""
        if self.win:
            self._draw_border()
            self._draw_title()
            self.win.refresh()

    def _erase(self):
        """Cancel all the window."""
        if self.win:
            self.win.erase()

    def resize(self, width, height):
        """Resize using fixed width and height."""
        self.height, self.width = height, width
        self.win.resize(self.height, self.width)
        self._refresh()


    def set_displayed(self, value: bool):
        self._is_displayed = value
    
    def is_displayed(self):
        return self._is_displayed



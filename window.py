
import curses

class Window():
    """Base class to display a window. This class is ment to be extendend
     by subclasses which will have to override the _refresh method to draw
     its content on the screen at each refresh and it can draw using the 
     draw_text and insert_character methods."""

    def __init__(self,title:str = ""):
        """Initialize the Window."""
        self.set_title(title)
        self.win = None
    
    def draw_ch(self, x : int, y : int, string : str) -> bool:
        """Display a text on the windows, respecting the window dimensions.
        Return if the drawn was sucessfully inside the window or else."""
        # Check if the text is in the bound of the window
        if x >= self.width - 2 or y > self.height:
            return False
        self.win.addch(y + 1, x + 1, string)
        return True

    def draw_text(self, x : int, y : int, string : str) -> bool:
        """Display a text on the windows, respecting the window dimensions.
        Return if the drawn was sucessfully inside the window or else."""
        # Check if the text is in the bound of the window
        if x >= self.width - 2 or y > self.height:
            return False

        for line in string.split("\n"):
            y += 1
            if y >= self.height:
                return False
            self.win.addnstr(y, x + 1, line, self.width - 2 - x)
        # This line would do the same but for some reason
        # It messes up the corner of all the windows
        # self.win.insstr(y + 1, x + 1, string)
        return True

    def get_shape(self):
        """Return the current dimension of the window as (width, height)."""
        return (self.width, self.height)

    def _set_father_windows(self, stdscr):
        """Set the father window."""
        self.father_windows = stdscr

    def _start(self):
        """Create the window, set it up, clean it and draw the result."""
        self.win = curses.newwin(1,1, 0, 0)
        self.win.nodelay(True)
        self.win.keypad(1)
        self.win.clear()
        self._resize()
        self._refresh()

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
        self.win.attrset(curses.color_pair(3)) 
        self.win.border(0,0,0,0,0,0,0,0)
        self.win.attrset(curses.A_NORMAL)

    def _draw_title(self):
        """Draw ther title on the top of the window."""
        self.draw_text(0,-1,self.title)

    def _refresh(self):
        """Method to be overwritten by the subclasses to add the content."""
        self._refresh_iter()

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

    def _resize(self):
        """Resize adapting to the father container."""
        height, width = self.father_windows.getmaxyx()
        self.resize(width, height - 1)

    def resize(self, width, height):
        """Resize using fixed width and height."""
        self.height, self.width = height, width
        self.win.resize(self.height, self.width)
        self._refresh()


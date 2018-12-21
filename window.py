
import curses

class Window():
    
    def __init__(self,title:str = ""):
        self.set_title(title)
        self.win = None

    def _set_father_windows(self, stdscr):
        self.father_windows = stdscr

    def _start(self):
        self._initialize_window()

    def _initialize_window(self,):
        self.win = curses.newwin(1,1, 0, 0)
        #self.win.attron(curses.color_pair(1))
        self.win.timeout(100)
        self.win.keypad(1)
        self.win.clear()
        self._resize()
        self._refresh()

    def get_title(self):
        return self.title

    def set_title(self,new_title : str):
        self.title = " " + new_title.strip() + " "

    def draw_text(self, x : int, y : int, string : str):
        self.win.addnstr(y + 1, x + 1, string, self.width - 3)

    def _move_window(self, new_x, new_y):
        """Move the windows so that the upper left corner is at new_x and new_y"""
        self.win.mvwin(new_y, new_x)

    def _draw_border(self):
        self.win.attrset(curses.color_pair(2)) 
        self.win.border(0,0,0,0,0,0,0,0)
        self.win.attrset(curses.A_NORMAL)

    def _draw_title(self):
        self.draw_text(0,-1,self.title)

    def _refresh(self):
        if self.win:
            self._draw_border()
            self._draw_title()
            self.win.refresh()

    def _erase(self):
        if self.win:
            self.win.erase()

    def _resize(self):
        height, width = self.father_windows.getmaxyx()
        self.resize(width, height - 1)

    def resize(self, width, height):
        self.height, self.width = height, width
        #self._erase()
        self.win.resize(self.height, self.width)
        self._refresh()


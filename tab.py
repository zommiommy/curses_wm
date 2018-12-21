
import curses
from window import Window

class Tab():
    def __init__(self, title: str):
        self.title = title
        self.window = None

    def _start(self):
        if self.window:
            self.window._start()

    def _set_father_windows(self, stdscr):
        self.father_windows = stdscr
        if self.window:
            self.window._set_father_windows(self.father_windows)

    def set_window(self, window: Window):
        if self.window:
            self.window._erase()
        self.window = window

    def set_title(self, new_title: str):
        self.title = new_title.strip()

    def get_title(self):
        return self.title

    def _refresh(self):
        if self.window:
            self.window._refresh()

    def _resize(self):
        if self.window:
            self.window._resize()

    def _erase(self):
        if self.window:
            self.window._erase()
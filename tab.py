
import curses
from window import Window
from wrapt import synchronized

class Tab():
    def __init__(self, title: str):
        self.title = title
        self.window = None
        self._is_displayed = False
        self.error_state = False

    def _start(self):
        if self.window:
            self.window._start()

    def set_error_state(self, error_state : bool):
        self.error_state = error_state

    def set_window(self, window: Window):
        if self.window:
            self.window._erase()
        self.window = window

    def set_displayed(self, value: bool):
        self._is_displayed = value
        if self.window:
            self.window.set_displayed(value)
    
    def is_displayed(self):
        return self._is_displayed

    def set_title(self, new_title: str):
        self.title = new_title.strip()

    def get_title(self):
        return self.title

    @synchronized
    def _refresh(self):
        if self.window:
            self.window._refresh()

    def resize(self, width : int, height : int):
        if self.window:
            self.window.resize(width, height)

    def _erase(self):
        if self.window:
            self.window._erase()
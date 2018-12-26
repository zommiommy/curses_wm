
import curses
from window import Window
from wrapt import synchronized

class TextBox(Window):

    def __init__(self,title:str = ""):
        """Initialize the Text Box."""
        super().__init__(title)
        self.text = ""
        self.x = 0
        self.y = 0

    def set_text(self, x : int, y : int, text : str):
        self.text = text
        self.x = x
        self.y = y
        self._refresh()

    @synchronized
    def _refresh(self):
        if self._is_displayed:
            self.draw_text(self.x, self.y, self.text)
            self._refresh_iter()

import curses
from window import Window
from wrapt import synchronized

class TextBox(Window):

    def __init__(self,title:str = ""):
        """Initialize the Text Box."""
        super().__init__(title)
        self.texts = []

    def set_text(self, x : int, y : int, text : str) -> None:
        self.texts = [{"x":x,"y":y,"text":text}]
        # self._refresh()

    def add_text(self, x : int, y : int, text : str) -> None:
        self.texts.append({"x":x,"y":y,"text":text})    
        # self._refresh()

    @synchronized
    def _refresh(self) -> None:
        for t in self.texts:
            self.draw_text(t["x"], t["y"], t["text"])
        self._refresh_iter()
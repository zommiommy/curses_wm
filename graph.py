
import curses
from window import Window


class Graph(Window):

    def __init__(self,title:str = "", draw_symbol : str = ".", round_number : int = 3):
        """Initialize the Graph."""
        super().__init__(title)
        self.points = [0]
        self.draw_symbol = draw_symbol
        self.round_number = round_number

    def add_point(self, value : int):
        self.points = self.points[1:] + [value]

    
    def resize(self, width, height):
        # pad the points to the new dim
        if len(self.points) < width:
            # if the new width is bigger than the buffer then pad the head with zeros
            self.points = [0] * (width - len(self.points)) + self.points
        else:
            # else select the readable data from the end
            self.points = self.points[-width:]

        super().resize(width,height)

    def _print_axis(self, min : int, max : int):
        M = str(round(max,self.round_number))
        m = str(round(min,self.round_number))
        x = self.width - 1
        y = self.height - 3
        self.draw_text(x - len(M), 0,M)
        self.draw_text(x - len(m), y, m)

    def _refresh(self):
        self.win.attrset(curses.color_pair(5)) 
        self._erase()
        M = max(self.points)
        m = min(self.points)
        delta = M - m
        if delta != 0:
            coeff = (self.height - 3) / delta

            for x, point in enumerate(self.points[:self.width]):
                y = self.height - 3 - int((point - m) * coeff)
                self.draw_text(x, y, self.draw_symbol)

        else:
            y = int((self.height - 3) / 2)
            for x, _ in enumerate(self.points[:self.width]):
                self.draw_text(x, y, self.draw_symbol)

        self._print_axis(m,M)   

        self.win.attrset(curses.A_NORMAL)
        self._refresh_iter()
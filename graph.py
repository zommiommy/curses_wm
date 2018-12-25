
import curses
from colours import GraphColour, GraphLegendColour, CentralLineColour
from window import Window


class Graph(Window):

    def __init__(self,title:str = "", draw_symbol : str = ".", legend_format : str = "{number:.2f}", momentum_rate : float = 0.9999, dot_step : int = 8):
        """Initialize the Graph."""
        super().__init__(title)
        self.points = [0]
        self.draw_symbol = draw_symbol
        self.legend_format = legend_format
        self.momentum_rate = momentum_rate
        self.dot_step = dot_step
        self.maximum = 0
        self.minimum = 0

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

    def _print_central_line(self):
        with CentralLineColour(self.win):
            for i in range(self.get_first_col(),self.get_last_col() + 1, self.dot_step):
                self.draw_text(i, self.get_mid_row(), self.draw_symbol)
            

    def _print_axis(self):
        maxi = self.legend_format.format(number=self.maximum)
        mini = self.legend_format.format(number=self.minimum)
        midl = int((self.maximum - self.minimum) / 2)
        midl = self.legend_format.format(number=midl)

        with GraphLegendColour(self.win): 
            self.draw_text(self.get_last_col() - len(maxi), self.get_first_row(), maxi)
            self.draw_text(self.get_last_col() - len(midl), self.get_mid_row(), midl)
            self.draw_text(self.get_last_col() - len(mini), self.get_last_row(), mini)

    def _momentum_update(self, value, new_value):
        return value * self.momentum_rate + (1 - self.momentum_rate) * new_value

    def _update_max_min(self):
        # Update the maximum
        new_max =  max(self.points)
        if new_max >= self.maximum:
            self.maximum = new_max
        else:
            self.maximum = self._momentum_update(self.maximum,new_max)
        # Update the minimum
        new_min =  min(self.points)
        if new_min <= self.minimum:
            self.minimum = new_min
        else:
            self.minimum = self._momentum_update(self.minimum,new_min)

    def _draw_graph(self):
        with GraphColour(self.win):
            delta =  self.maximum - self.minimum
            
            if delta != 0:
                coeff = self.get_last_row() / delta

                for x, point in enumerate(self.points[:self.width]):
                    y = self.get_last_row() - int((point - self.minimum) * coeff)
                    self.draw_text(x, y, self.draw_symbol)

            else:
                for x in range(self.width):
                    self.draw_text(x, self.get_mid_row(), self.draw_symbol)


    def _refresh(self):
        self._erase()
        self._update_max_min()
        self._print_central_line()
        self._draw_graph()
        self._print_axis()
        self._refresh_iter()
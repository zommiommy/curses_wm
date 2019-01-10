
import curses
from typing import List, Dict, Union

from .colours import CentralLineColour, GraphColour, GraphLegendColour
from .window import Window


class Graph(Window):

    symbols = {
        (0,0): "⠉",
        (0,1): "⠑",
        (0,2): "⠡",
        (1,0): "⠊",
        (1,1): "⠒",
        (1,2): "⠢",
        (2,0): "⠌",
        (2,1): "⠔",
        (2,2): "⠤"
    }

    def __init__(self,title : str = "", **kwargs):
        """Initialize the Graph.
        Graph(
        title:str = "",
        draw_symbol : str = ".",
        legend_format : str = "{number:.2f}",
        momentum_rate : float = 0.9999,
        dot_step : int = 8
        )
        """
        super().__init__(title, **kwargs)
        self.points : List[int] = []
        self.draw_symbol : str = kwargs.get("draw_symbol",".")
        self.legend_format : str = kwargs.get("legend_format","{number:.2f}")
        self.momentum_rate : float = kwargs.get("momentum_rate",0.9999)
        self.dot_step : int = kwargs.get("dot_step",8)
        self.maximum = -float("Inf")
        self.minimum = float("Inf")

    def add_point(self, value : int) -> None:
        """Add a point to the graph."""
        self.points = self.points[1:] + [value]

    
    def resize(self, width : int, height : int) -> None:
        """ resize(width : int, height : int) -> None
            Resize the graph to the new dimensions."""
        # pad the points to the new dim
        super().resize(width,height)

        # Calculate things using the double of width since braille symbols can rappresent 2 points
        width = 2 * width
        if len(self.points) < width:
            # if the new width is bigger than the buffer then pad the head with zeros
            self.points = [0] * (width - len(self.points)) + self.points
        else:
            # else select the readable data from the end
            self.points = self.points[-width:]


    def _print_central_line(self) -> None:
        with CentralLineColour(self.win):
            for i in range(self.get_first_col(),self.get_last_col() + 1, self.dot_step):
                self.draw_text(i, self.get_mid_row(), self.draw_symbol)
            

    def _print_axis(self) -> None:
        maxi : str = self.legend_format.format(number=self.maximum)
        mini : str = self.legend_format.format(number=self.minimum)
        midl : float = (self.maximum + self.minimum) / 2
        midl : str = self.legend_format.format(number=midl)

        with GraphLegendColour(self.win): 
            self.draw_text(self.get_last_col(1 - len(maxi)) , self.get_first_row(), maxi)
            self.draw_text(self.get_last_col(1 - len(midl)) , self.get_mid_row()  , midl)
            self.draw_text(self.get_last_col(1 - len(mini)) , self.get_last_row() , mini)

    def _momentum_update(self, value : float, new_value : float) -> float:
        return value * self.momentum_rate + (1 - self.momentum_rate) * new_value

    def _update_max_min(self) -> None:
        # Update the maximum
        new_max = max(self.points)
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

    def _draw_graph(self) -> None:
        """draw on the screen the graph, this method check for the special cases"""
        with GraphColour(self.win):
            delta = (self.maximum - self.minimum)
            if delta != 0:
                self._print_graph(delta)
            else:
                self._print_zero_line()

    def _get_y_scaling_coeff(self, delta) -> float:
        """Return the coefficient to transform a point to a y coordinate"""
        # work with 3 times the y space since brailles symbols can print 3 rows
        return 3 * (self.get_last_row() - 1) / delta

    def _convert_point(self, point, coeff):
        """Convert a point to a y coordinate"""
        return (3*self.get_last_row()) - int((point - self.minimum) * coeff)

    def _get_y_points(self, coeff)-> List[int]:
        """Convert all the points to y coordinates"""
        return [self._convert_point(point,coeff) for point in self.points]

    def _get_symbol(self, y1, y2):
        """Given the pair of points return the symbols that correspond to them"""
        # If the values are in the same 3-chunk then assign them the related symbol
        if abs(y1-y2) <= 3:
            return self.symbols[(y1%3,y2%3)] 
        # Else if the second point is in a lower chunk than the first one return a symbol with the second point on the lower row
        elif y1 < y2:
            return self.symbols[(y1%3,2)]
        # Else if the second point is in a higher chunk than the first one return a symbol with the second point on the higher row
        else:
            return self.symbols[(y1%3,0)]

    def _pair_of_coordinates(self, points):
        """return a generator that returns pair of points in the form x, (y1, y2). the Iteration_0[y2] != Iteration_1[y1]"""
        return enumerate(zip(points[::2],points[1::2]))

    def _print_graph(self, delta):
        """Print on the screen the actual graph"""
        coeff = self._get_y_scaling_coeff(delta)
        points = self._get_y_points(coeff)
        for x, (y1, y2) in self._pair_of_coordinates(points):
            self.draw_text(x, int(y1/3), self._get_symbol(y1,y2))


    def _print_zero_line(self):
        """Print a central line of dots, this is used when the points ar all the same and max == min."""        
        for x in range(self.width):
            self.draw_text(x, self.get_mid_row(), self.symbols[(1,1)])

    def _refresh_overriden(self) -> None:
        self._update_max_min()
        self._print_central_line()
        self._draw_graph()
        self._print_axis()

    def get_default_min_dim(self) -> Dict[str,Union[float,int]]:
        """Return the MINIMUM dimension at which the window has sense, 3 means that smaller than 3x3 the window is useless."""
        if self.display_border:
            return {"x":5,"y":5}
        else:
            return {"x":3,"y":3}
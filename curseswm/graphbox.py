
import curses
import random
from typing import Dict, List, Union

from .braille import braille_symbols
from .colours import CentralLineColour, GraphAxisColour, graph_colours, Colour
from .graph import Graph
from .horribleworkaround import horrible_workaround
from .window import Window


def flatten(ll):
    """convert a list of list to a list"""
    return [x for l in ll for x in l]

class GraphBox(Window):

    def __init__(self,title : str = "", **kwargs):
        """Initialize the Graph.
        Graph(
        title:str = "",
        draw_symbol : str = ".",
        legend_format : str = "{number:.2f}",
        dot_step : int = 8
        )
        """
        super().__init__(title, **kwargs)
        self.graphs : List[Graph] = []
        self.draw_symbol : str = kwargs.get("draw_symbol",".")
        self.legend_format : str = kwargs.get("legend_format","{number:.2f}")
        self.dot_step : int = kwargs.get("dot_step",8)
        self.maximum = -float("Inf")
        self.minimum = float("Inf")
        self.colour_index = -1


    def _get_random_colour(self) -> int:
        c = list(graph_colours.values())
        self.colour_index = (self.colour_index + 1) % len(c)
        return c[self.colour_index]

    def _start(self):
        [g.set_colour(self._get_random_colour()) for g in self.graphs]
        return super()._start()

    def add_graph(self, graph : Graph) -> None:
        """Add a point to the graph."""
        self.graphs.append(graph)

    def _update_max_min(self) -> None:
        [x._update_max_min() for x in self.graphs]
        self.maximum = max([x.maximum for x in self.graphs])
        self.minimum = min([x.minimum for x in self.graphs])
    
    def _print_zero_line(self):
        """Print a central line of dots, this is used when the points are all the same and max == min."""
        if len(self.graphs) != 0:
            c = self.graphs[-1].get_colour()
        else:
            c = Colour(graph_colours["blue"])
        with c(self.win):
            for x in range(self.width):
                self.draw_text(x, self.get_mid_row(), "⠒")

    def resize(self, width : int, height : int) -> None:
        """ resize(width : int, height : int) -> None
            Resize the graph to the new dimensions."""
        # pad the points to the new dim
        super().resize(width,height)
        # Update all the subgraphs
        [g.resize(width) for g in self.graphs]
        

    def _print_central_line(self) -> None:
        with CentralLineColour(self.win):
            for i in range(self.get_first_col(),self.get_last_col() + 1, self.dot_step):
                self.draw_text(i, self.get_mid_row(), self.draw_symbol)
            

    def _print_axis(self) -> None:
        maxi : str = self.legend_format.format(number=self.maximum)
        mini : str = self.legend_format.format(number=self.minimum)
        midl : float = (self.maximum + self.minimum) / 2
        midl : str = self.legend_format.format(number=midl)

        with GraphAxisColour(self.win): 
            self.draw_text(self.get_last_col(1 - len(maxi)) , self.get_first_row(), maxi)
            self.draw_text(self.get_last_col(1 - len(midl)) , self.get_mid_row()  , midl)
            self.draw_text(self.get_last_col(1 - len(mini)) , self.get_last_row() , mini)

    def _draw_graph(self) -> None:
        """draw on the screen the graph, this method check for the special cases"""
        self._update_max_min()
        delta = (self.maximum - self.minimum)
        if delta > 0:
            self._print_graph(delta)
        else:
            self._print_zero_line()

    def _get_y_scaling_coeff(self, delta) -> float:
        """Return the coefficient to transform a point to a y coordinate"""
        # work with 3 times the y space since brailles symbols can print 3 rows
        return 3 * (self.get_last_row() - 1) / delta

    @horrible_workaround
    def _print_legend(self) -> None:
        index = self.get_last_col()

        # Get the last cell occupied by the title
        min_index = self.get_title_len() + 1
        
        self.win.addstr(0,index," ")

        for g in self.graphs:
            name = g.name
            index -= (len(name) + 1)
            # TODO print partial names
            if min_index > index:
                return
            # Print the name of the graph
            with g.get_colour()(self.win):
                self.win.addstr(0,index," " + name)


    def _convert_point(self, points : List[float], coeff : float) -> List[int]:
        """Convert a point to a y coordinate"""
        return [(3*self.get_last_row()) - int((point - self.minimum) * coeff) for point in points]

    def _get_columns(self, coeff : float) -> List[List[int]]:
        """return the points in the column in the form [[y1,y2,y3,...,yn],[y1,y2,y3,...,yn],...]"""
        return list(zip(*[self._convert_point(g.points,coeff) for g in self.graphs]))

    def _get_double_columns(self, coeff : float) -> List[List[List[int]]]:
        """Return a list of couple of columns in the form [c1,c2] so it's [[y1,y2,y3,...,yn],[y1,y2,y3,...,yn]
        so the final list is [[[y1,y2,y3,...,yn],[y1,y2,y3,...,yn]],[[y1,y2,y3,...,yn],[y1,y2,y3,...,yn]],...]"""
        points = self._get_columns(coeff)
        return list(zip(points[::2],points[1::2]))

    def _print_graph(self, delta):  
        """Print on the screen the actual graph"""
        coeff = self._get_y_scaling_coeff(delta)
        for x, double_column in enumerate(self._get_double_columns(coeff)):
            self._draw_double_column(x, double_column)

    def _draw_double_column(self,graph_x : int, double_column : List[List[int]]) -> None:
        # If two points land on the same 2x3 box then they must be displayed 
        d = {}
        for x, y_values in enumerate(double_column):
            for i, y3 in enumerate(y_values):
                key = int(y3/3)
                y = y3 % 3
                symbol = d.setdefault(key, {
                                                "matrix":[[0,0],[0,0],[0,0]],
                                                "colour": None
                                            })
                symbol["colour"] = self.graphs[i].get_colour()
                matrix = symbol["matrix"]
                matrix[y][x] = 1
                symbol["matrix"] = matrix

        # Draw each 2x3 box
        for y, symbol in d.items():
            matrix = symbol["matrix"]
            glyph = braille_symbols[str(matrix)]
            colour = symbol["colour"]
            with colour(self.win):
                self.draw_text(graph_x, y, glyph)

    def _refresh_overridden(self) -> None:
        self._update_max_min()
        self._print_central_line()
        self._draw_graph()
        self._print_axis()
        self._print_legend()

    def get_default_min_dim(self) -> Dict[str,Union[float,int]]:
        """Return the MINIMUM dimension at which the window has sense, 3 means that smaller than 3x3 the window is useless."""
        if self.display_border:
            return {"x":5,"y":5}
        else:
            return {"x":3,"y":3}

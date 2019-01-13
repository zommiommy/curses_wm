
import curses
from typing import List, Dict, Union


from .colours import Colour

class Graph():

    def __init__(self, name : str = ""):
        self.name = name
        self.points : List[int] = [ ] 
        self.maximum = -float("Inf")
        self.minimum = float("Inf")
        self.momentum_rate = 0.999
        self.colour = None

    def add_point(self, value : int) -> None:
        """Add a point to the graph."""
        self.points = self.points[1:] + [value]

    def set_colour(self, colour : Colour) -> None:
        self.colour = Colour(colour)

    def get_colour(self) -> Colour:
        return self.colour

    def get_last_point(self) -> float:
        if len(self.points) >= 1:
            return self.points[-1]
        else:
            return float("nan")

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

    def resize(self, width) -> None:
        # Calculate things using the double of width since braille symbols can rappresent 2 points
        width = 2 * width
        if len(self.points) < width:
            # if the new width is bigger than the buffer then pad the head with zeros
            self.points = [0] * (width - len(self.points)) + self.points
        else:
            # else select the readable data from the end
            self.points = self.points[-width:]
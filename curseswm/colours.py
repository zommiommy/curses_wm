
import curses

colour_pair_index = 0

colours = {
            "blue":curses.COLOR_BLUE,
            "yellow":curses.COLOR_YELLOW,
            "green":curses.COLOR_GREEN,
            "red":curses.COLOR_RED,
            "white":curses.COLOR_WHITE,
            "magenta":curses.COLOR_MAGENTA,
            "cyan":curses.COLOR_CYAN
        }           

graph_colours = {}

class Colour():
    def __init__(self, color_pair_index : int,standout : bool = False):
        self.color_pair_index = color_pair_index
        self.standout = standout

    def __call__(self, window):
        self.window = window
        return self

    def __enter__(self):
        self.window.attrset(curses.color_pair(self.color_pair_index))
        if self.standout:
            self.window.attron(curses.A_STANDOUT)

    def __exit__(self, type, value, traceback):
        self.window.attrset(curses.A_NORMAL)


def register_new_colour_pair(c1,c2) -> int:
    global colour_pair_index
    colour_pair_index += 1
    curses.init_pair(colour_pair_index, c1, c2)
    return colour_pair_index

def initialize_colours():
    global graph_colours
    register_new_colour_pair(curses.COLOR_WHITE, curses.COLOR_BLACK) # 1
    register_new_colour_pair(curses.COLOR_RED  , curses.COLOR_BLACK) # 2
    register_new_colour_pair(curses.COLOR_CYAN , curses.COLOR_BLACK) # 3
    register_new_colour_pair(curses.COLOR_CYAN , curses.COLOR_RED)   # 4

    for name, colour in colours.items():
        graph_colours[name] = register_new_colour_pair(colour, curses.COLOR_BLACK)


BorderColour = Colour(3)
TextColour   = Colour(1)
ErrorColour  = Colour(2)
ErrorColour  = Colour(2)
HighlightErrorColour = Colour(4,standout=True)
HighlightColour = Colour(3,standout=True)
NormalColour = Colour(1)
CentralLineColour = Colour(1)
GraphAxisColour = Colour(1)
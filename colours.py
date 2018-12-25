
import curses

def initialize_colours():
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED  , curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN , curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN , curses.COLOR_RED)
    curses.init_pair(5, curses.COLOR_YELLOW , curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE , curses.COLOR_BLACK)

class Colour():
    def __init__(self, window):
        self.window = window

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, type, value, traceback):
        self.window.attrset(curses.A_NORMAL)

class BorderColour(Colour):
    def __init__(self, window):
        super().__init__(window)

    def __enter__(self):
        self.window.attrset(curses.color_pair(3))

class TextColour(Colour):
    def __init__(self, window):
        super().__init__(window)

    def __enter__(self):
        self.window.attrset(curses.color_pair(1))

class ErrorColour(Colour):
    def __init__(self, window):
        super().__init__(window)

    def __enter__(self):
        self.window.attrset(curses.color_pair(2))

class HighlightErrorColour(Colour):
    def __init__(self, window):
        super().__init__(window)

    def __enter__(self):
        self.window.attrset(curses.color_pair(4))
        self.window.attron(curses.A_STANDOUT)

class HighlightColour(Colour):
    def __init__(self, window):
        super().__init__(window)

    def __enter__(self):
        self.window.attrset(curses.color_pair(3))
        self.window.attron(curses.A_STANDOUT)

class GraphColour(Colour):
    def __init__(self, window):
        super().__init__(window)

    def __enter__(self):
        self.window.attrset(curses.color_pair(5))

class GraphLegendColour(Colour):
    def __init__(self, window):
        super().__init__(window)

    def __enter__(self):
        self.window.attrset(curses.color_pair(5))

class NormalColour(Colour):
    def __init__(self, window):
        super().__init__(window)

    def __enter__(self):
        self.window.attrset(curses.A_NORMAL)

    
class CentralLineColour(Colour):
    def __init__(self, window):
        super().__init__(window)

    def __enter__(self):
        self.window.attrset(curses.color_pair(6))

    
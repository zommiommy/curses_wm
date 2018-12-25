

import sys
import curses
import colours
from tab import Tab
from hbox import HBox
from vbox import VBox
from time import sleep
from graph import Graph
from window import Window
from screen import Screen
from textbox import TextBox
from threading import Thread
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_RESIZE

class CLI(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.screen = Screen()
        self.tab_list = []
        self.tab_index = 0
        self.key_handlers = {
            ord("q"): self._quit,
            KEY_RESIZE: self._resize,
            KEY_LEFT:   self._move_left,
            KEY_RIGHT:  self._move_right
        }

    def _quit(self):
        self.screen.clean_up_terminal()
        sys.exit(0)
        

    def _initialize_tabs(self):
        """Pass the reference of the screen to all the tabs and start them"""
        [tab._start() for tab in self.tab_list]


    def _set_error_attr(self, tab, index):
        if index == self.tab_index:
            if tab.error_state:
                return colours.HighlightErrorColour
            else:
                return colours.HighlightColour
        else:
            if tab.error_state:
                return colours.ErrorColour
            else:
                return colours.TextColour

    def _print_tab(self, x, y, tab, index):
        # print the initial space
        with colours.NormalColour(self.stdscr):
            self.stdscr.addstr(y, x, " ")
        x += 1
        # Set the style of the tile and print the tab name
        style = self._set_error_attr(tab, index)
        with style(self.stdscr):
            self.stdscr.addstr(y, x, tab.title)
        # Return the updated writing position
        return x + len(tab.title)


    def _print_status_bar(self):
        """Print the status bar."""
        last_line = self.height - 1
        x = 0
        for index, tab in enumerate(self.tab_list):
            x = self._print_tab(x, last_line, tab, index)

    def _move_left(self):
        """Move the tab_index to the next on the left and display that tab."""
        if self.tab_index == 0:
            return
        self._erase()
        self.tab_index -= 1
        self._refresh()
    
    def _move_right(self):
        """Move the tab_index to the next on the right and display that tab."""
        if self.tab_index == len(self.tab_list) - 1:
            return
        self._erase()
        self.tab_index += 1
        self._refresh()
    

    def _erase(self):
        """Clear the screen"""
        if self.stdscr:
            self.stdscr.erase()
            # Need to erase all the windows else there will be resize borders on other tabs
            [tab._erase() for tab in self.tab_list]

    def _refresh(self):
        """Refresh the screen and the tab on sight"""
        self._print_status_bar()
        self.stdscr.refresh()
        self.tab_list[self.tab_index]._refresh()
        
    def _resize(self):
        """Erase the screen, call the resize method of all the tabs and update the CLI dimension"""
        self.height, self.width = self.stdscr.getmaxyx()
        self._erase()
        [tab.resize(self.width, self.height - 1) for tab in self.tab_list]
        self._refresh()
        
    def add_tab(self, tab: Tab):
        """add a tab to the cli"""
        self.tab_list.append(tab)

    def _run(self):
        """Actual run function"""
        self._print_status_bar()
        while True:
            self._refresh()
            x = self.stdscr.getch()
            if x in self.key_handlers:
                self.key_handlers[x]()

    def run(self):
        """wrapper so the exceptions can be displayed"""
        # Start the cli
        self.stdscr = self.screen.start()
        # save the current dim
        self.height, self.width = self.stdscr.getmaxyx()
        # Start all the tabs
        self._initialize_tabs()
        # Draw all the tabs
        self._resize()
        try:
            self._run()
        except KeyboardInterrupt:
            self.screen.clean_up_terminal()
        finally:
            self.screen.clean_up_terminal()


    

if __name__ == "__main__":

    from math import sin

    cli = CLI()

    tab = Tab("Overview")
    cli.add_tab(tab)

    tab2 = Tab("Networks")
    cli.add_tab(tab2)

    tab3 = Tab("Threads")
    cli.add_tab(tab3)


    w0 = TextBox("Timer")
    w1 = Window("Windows 1")
    w2 = Window("Windows 2")
    w3 = Window("Windows 3")
    w4 = TextBox("TextBox 4")
    g = Graph("Graph Test")
    w6 = Window("Windows 6")

    w4.set_text(w4.get_first_col() + 2,w4.get_first_row() + 2,"Test Text 3")
    
    v = VBox()
    v.add_window(g,weight=1)

    h = HBox()
    h.add_window(w4,weight=1)
    h.add_window(w0,weight=1)

    v.add_window(h,weight=2)

    tab.set_window(v)

    tab2.set_window(w2)

    tab3.set_window(w3)

    cli.start()
    
    sleep(1)

    i = 0
    while True:
        w0.set_text(w0.get_first_col(),w0.get_first_row(),"Time Enlapsed %d"%i)
        tab2.set_error_state(i % 2 == 1)
        g.add_point(sin(i/20))
        i += 1
        sleep(1/10)
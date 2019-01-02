

import sys
import curses
from time import sleep
from threading import Thread
from wrapt import synchronized
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_RESIZE

from . import colours
from .tab import Tab
from .window import Window
from .screen import Screen

class CLI(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.screen = Screen()
        self.tab_list = []
        self.tab_index = 0
        self.refresh_rate = None
        self.key_handlers = {
            ord("q"): self._quit,
            KEY_RESIZE: self._resize,
            KEY_LEFT:   self._move_left,
            KEY_RIGHT:  self._move_right
        }

    def _quit(self) -> None:
        self.screen.clean_up_terminal()
        sys.exit(0)
        

    def _initialize_tabs(self) -> None:
        """Pass the reference of the screen to all the tabs and start them"""
        [tab._start() for tab in self.tab_list]


    def _set_error_attr(self, tab : Tab, index : int) -> None:
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

    def _print_tab(self, x : int, y : int, tab : Tab, index : int) -> None:
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


    def _print_status_bar(self) -> None:
        """Print the status bar."""
        last_line = self.height - 1
        x = 0
        for index, tab in enumerate(self.tab_list):
            x = self._print_tab(x, last_line, tab, index)

    def _move_left(self) -> None:
        """Move the tab_index to the next on the left and display that tab."""
        if self.tab_index == 0:
            return
        self._erase()
        self.tab_index -= 1
    
    def _move_right(self) -> None:
        """Move the tab_index to the next on the right and display that tab."""
        if self.tab_index == len(self.tab_list) - 1:
            return
        self._erase()
        self.tab_index += 1
    

    def _erase(self) -> None:
        """Clear the screen"""
        if self.stdscr:
            self.stdscr.erase() 
            # Need to erase all the windows else there will be resize borders on other tabs
            [tab._erase() for tab in self.tab_list]

    @synchronized
    def _refresh(self) -> None:
        """Refresh the screen and the tab on sight"""
        self._print_status_bar()
        self.stdscr.refresh()
        self.tab_list[self.tab_index]._refresh()
        
    def _resize(self) -> None:
        """Erase the screen, call the resize method of all the tabs and update the CLI dimension"""
        self.height, self.width = self.stdscr.getmaxyx()
        self._erase()
        [tab.resize(self.width, self.height - 1) for tab in self.tab_list]
        self._refresh()
        
    def add_tab(self, tab: Tab) -> None:
        """add a tab to the cli"""
        self.tab_list.append(tab)

    def set_refresh_rate(self, refresh_rate : int) -> None:
        self.refresh_rate = refresh_rate
        if self.screen:
            self.screen.set_refresh_rate(refresh_rate)

    def _run(self) -> None:
        """Actual run function"""
        while True:
            self._refresh()
            x = self.stdscr.getch()
            if x in self.key_handlers:
                self.key_handlers[x]()

    def run(self) -> None:
        """wrapper so the exceptions can be displayed"""
        # Start the cli
        self.stdscr = self.screen.start()
        if self.refresh_rate:
            self.screen.set_refresh_rate(self.refresh_rate)
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


   
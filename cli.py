

import sys
import curses
from tab import Tab
from time import sleep
from window import Window
from hbox import HBox
from vbox import VBox
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_RESIZE

class CLI():
    def __init__(self):
        self.stdscr = None
        self.tab_list = []
        self.tab_index = 0
        self.key_handlers = {
            ord("q"): self._quit,
            KEY_RESIZE: self._resize,
            KEY_LEFT:   self._move_left,
            KEY_RIGHT:  self._move_right
        }

    def _start(self):
        """Initialize the curses and the terminal."""
        # Setup the screen
        self.stdscr = curses.initscr()
        # Enable colors
        try:
            curses.start_color()
        except:
            pass
        # Disable key display on screen
        curses.noecho()
        # Enable Callbacks for keys so they act as interrupts
        curses.cbreak()
        # Disable the cursor visibility
        curses.curs_set(0)
        # Enable the use of KEY_UP and special keys as variables (keypad mode)
        self.stdscr.keypad(True)
        # add colour
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
        # save the current dim
        self.height, self.width = self.stdscr.getmaxyx()

    def _clean_up_terminal(self):
        """reset the terminal to the previous settings."""
        if self.stdscr:
            # Disable the Keypad mode
            self.stdscr.keypad(False)
            # Renable caracters echoing
            curses.echo()
            # Disable the interrupts
            curses.nocbreak()
            # Restore the terimnal to it's orginial operating mode
            curses.endwin()

    def __del__(self):
        """On destruction clear the terminal"""
        self._clean_up_terminal()

    def run(self):
        """wrapper so the exceptions can be displayed"""
        self._start()
        self._initialize_tabs()
        self._start_all_windows()
        try:
            self._run()
        finally:
            self._clean_up_terminal()

    def _quit(self):
        self._clean_up_terminal()
        sys.exit(0)
        

    def _pad_to_width(self, string):
        """Pad a string with spaces till the string is as long as the screen"""
        return string  + " " * (self.width - len(string) - 2)

    def _initialize_tabs(self):
        """Pass the reference of the screen to all the tabs"""
        [tab._set_father_windows(self.stdscr) for tab in self.tab_list]

    def _start_all_windows(self):
        """Create all the window of all the tabs"""
        [tab._start() for tab in self.tab_list]

    def _print_status_bar(self):
        """Print the status bar."""
        titles = [tab.title for tab in self.tab_list]
        string = " ".join(titles)
        last_line = self.height - 1

        l = 0
        self.stdscr.attrset(curses.color_pair(1)) 
        for title in titles[ : self.tab_index]:
            self.stdscr.addstr(last_line, l, " " + title)
            l += len(title) + 1

        self.stdscr.addstr(last_line, l, " " )
        l += 1
        self.stdscr.attrset(curses.color_pair(2)) 
        self.stdscr.attron(curses.A_STANDOUT)

        title = titles[self.tab_index]
        self.stdscr.addstr(last_line, l, title)
        l += len(title)

        self.stdscr.attrset(curses.color_pair(1)) 

        for title in titles[self.tab_index + 1:]:
            self.stdscr.addstr(last_line, l, " " + title)
            l += len(title) + 1
        self.stdscr.attrset(curses.A_NORMAL)

    def _move_left(self):
        # Clear the tab
        self._erase()
        self.tab_list[self.tab_index]._erase()
        # Update the index
        self.tab_index -= 1
        self.tab_index = max([0,self.tab_index])
        # Update
        self._refresh()
        self.tab_list[self.tab_index]._refresh()
    
    def _move_right(self):
        # Clear the tab
        self._erase()
        self.tab_list[self.tab_index]._erase()
        # Update the index
        self.tab_index += 1
        self.tab_index = min([len(self.tab_list) - 1,self.tab_index])
        # Update?
        self._refresh()
        self.tab_list[self.tab_index]._refresh()

    def _erase(self):
        """Clear the screen"""
        if self.stdscr:
            self.stdscr.erase()
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
        [tab._resize() for tab in self.tab_list]
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

    

if __name__ == "__main__":
    from multiprocessing import Process

    cli = CLI()

    tab = Tab("Overview")
    cli.add_tab(tab)

    tab2 = Tab("Networks")
    cli.add_tab(tab2)

    tab3 = Tab("Threads")
    cli.add_tab(tab3)


    w0 = Window("Windows 0")
    w1 = Window("Windows 1")
    w2 = Window("Windows 2")
    w3 = Window("Windows 3")
    w4 = Window("Windows 4")
    w5 = Window("Windows 5")
    w6 = Window("Windows 6")

    v = VBox()
    v.add_window(w0,1)

    h = HBox()
    h.add_window(w4,1)
    h.add_window(w5,1)

    v.add_window(h,1)

    tab.set_window(v)

    tab2.set_window(w2)

    tab3.set_window(w3)

    p = Process(target=cli.run)
    p.start()
    
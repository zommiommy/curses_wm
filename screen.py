
import curses

class Screen():

    def __init__(self):
        self.stdscr = None

    def start(self):
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
        # Make getkey non blocking
        self.stdscr.nodelay(True)
        # add colour
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED  , curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN , curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN , curses.COLOR_RED)

        return self.stdscr


    def clean_up_terminal(self):
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
        self.clean_up_terminal()
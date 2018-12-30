
import curses
import colours

class Screen():

    def __init__(self):
        self.stdscr = None

    def start(self, refresh_rate : int = 24):
        """Initialize the curses and the terminal."""
        # Setup the screen
        self.stdscr = curses.initscr()
        # Enable colors
        if curses.has_colors():
            curses.start_color()
        # Disable key display on screen
        curses.noecho()
        # Enable Callbacks for keys so they act as interrupts
        curses.cbreak()
        # Disable the cursor visibility
        curses.curs_set(0)
        # Enable the use of KEY_UP and special keys as variables (keypad mode)
        self.stdscr.keypad(True)
        # Make getkey non blocking
        # self.stdscr.nodelay(True)
        self.set_refresh_rate(refresh_rate)
        # add colour
        colours.initialize_colours()

        return self.stdscr

    def set_refresh_rate(self, refresh_rate : int) -> None:
        """Set the refresh rate of the CLI"""
        if self.stdscr:
            self.stdscr.timeout(int(1000 / refresh_rate))

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
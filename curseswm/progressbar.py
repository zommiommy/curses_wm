
import curses

from .window import Window
from .colours import *

class ProgressBar(Window):

    styles = {
        "htop":{
            "update_sequence":"|",
            "empty_seq":" ",
            "format": "{name} [{progress_bar}{empty_bar}{percentage:.1f}%]",
            "colour": TextColour
        },
        "apt-get":{
            "update_sequence":"#",
            "empty_seq":"-",
            "format": "{name}:[{percentage:.0f}%] [{progress_bar}{empty_bar}]",
            "colour": TextColour
        },
        "apt-get2":{
            "update_sequence":"0123456789#",
            "empty_seq":"-",
            "format": "{name}:[{percentage:.0f}%] [{progress_bar}{empty_bar}]",
            "colour": TextColour
        },
        "pacman":{
            "update_sequence":"#",
            "empty_seq":"-",
            "format": "{name} [{progress_bar}{empty_bar}] {percentage:.0f}%",
            "colour": TextColour
        },
        "smooth":{
            "update_sequence": " ▏▎▍▌▋▊▉█",
            "empty_seq":" ",
            "format": "{name} | {percentage:.1f}% | {progress_bar}{empty_bar}>",
            "colour": TextColour
        },
        "equal":{
            "update_sequence": "=",
            "empty_seq":".",
            "format": "{name} [{progress_bar}>{percentage:.1f}%{empty_bar}]",
            "colour": TextColour
        }
    }

    def __init__(self,name:str = "",title:str = "", **kwargs):
        """ProgressBar(
            name: str,
            title: str,
            style: str,
            update_sequence: str,
            empty_seq: str,
            format: str,
            colour: Colour)
        the format, empy_seq and update_sequence will be inherited from the default or chosen style if not specified."""
        # Set the default display_border to false
        kwargs.setdefault("display_border",False)
        super().__init__(title, **kwargs)
        self.name = name
        self.percentage : float = 0.0

        # Style setting
        self.style = self.styles[kwargs.get("style","smooth")]
        # Style expansion
        self.update_sequence = kwargs.get("update_sequence",self.style["update_sequence"])
        self.empty_seq = kwargs.get("empty_seq",self.style["empty_seq"])
        self.format = kwargs.get("format",self.style["format"])
        self.colour = kwargs.get("colour",self.style["colour"])

    def set_percentage(self, percentage : float) -> None:
        """Set the percentage of completion, it must be a float between 0.0 and 1.0 """
        if percentage < 0:
            percentage = 0
        elif percentage > 1:
            percentage = 1
        self.percentage = percentage

    def _refresh_overriden(self) -> None:
        """Draw the progress bar on the screen"""

        # Calculate the total space for the bar
        text_range = self.get_last_col() - self.get_first_col() + 1

        # subtract the space for the formatting from the bar space
        base_string = self.format.format(name=self.name,progress_bar="",empty_bar="",percentage=100*self.percentage)
        text_range -= len(base_string)

        text_subrange = text_range * len(self.update_sequence)

        index = int(text_subrange * self.percentage)

        fill_index = int(index / len(self.update_sequence))
        half_char = index % len(self.update_sequence)

        pbar = self.update_sequence[-1] * (fill_index)
        pbar += self.update_sequence[half_char]

        empty_bar = self.empty_seq * (text_range - fill_index - 1)

        output = self.format.format(name=self.name,progress_bar=pbar,empty_bar=empty_bar,percentage=100*self.percentage)

        with self.colour(self.win):
            self.draw_text(self.get_first_col(),self.get_first_row(), output)


    def get_default_max_dim(self) -> int:
        """Return the MAXIMUM dimension at which the window has sense, 3 means that bigger than 3x3 the window is useless."""
        if self.display_border:
            return 3
        else:
            return 1
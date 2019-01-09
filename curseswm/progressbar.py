
import curses

from .window import Window

class ProgressBar(Window):

    styles = {
        "htop":{
            "update_sequence":"|",
            "empty_seq":" ",
            "format": "{name} [{progress_bar}] {percentage:.1f}%"
        },
        "apt-get":{
            "update_sequence":"0123456789#",
            "empty_seq":"-",
            "format": "{name}:[{percentage:.0f}%] [{progress_bar}]"
        },
        "pacman":{
            "update_sequence":"#",
            "empty_seq":"-",
            "format": "{name} [{progress_bar}] {percentage:.0f}%"
        },
        "smooth":{
            "update_sequence": " ▏▎▍▌▋▊▉█",
            "empty_seq":" ",
            "format": "{name} |{progress_bar}> {percentage:.1f}%"
        },
    }

    def __init__(self,name:str = "",title:str = "", **kwargs):
        """Initialize the ProgressBar."""
        super().__init__(title, **kwargs)
        self.name = name
        self.percentage : float = 0.0

        # Style setting
        self.style = self.styles[kwargs.get("style",list(self.styles.keys())[0])]
        # Style expansion
        self.update_sequence = kwargs.get("update_sequence",self.style["update_sequence"])
        self._empty_seq = kwargs.get("empty_seq",self.style["empty_seq"])
        self.format = kwargs.get("format",self.style["format"])



    def set_update_sequence(self, sequence : str) -> None:
        """Set the sequence of symbols that the progress bar will iterate from left to right. There MUST be at least 1 char"""
        if 1 > len(sequence):
            return
        self.update_sequence = sequence

    def set_empty_sequence(self, empty_seq : str) -> None:
        """Set the sequence for the empty part of the bar"""
        if len(empty_seq) < 1:
            return 
        self._empty_seq = empty_seq

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
        base_string = self.format.format(name=self.name,progress_bar="",percentage=100*self.percentage)
        text_range -= len(base_string)

        text_subrange = text_range * len(self.update_sequence)

        index = int(text_subrange * self.percentage)

        fill_index = int(index / len(self.update_sequence))
        half_char = index % len(self.update_sequence)

        pbar = self.update_sequence[-1] * (fill_index)
        pbar += self.update_sequence[half_char]
        pbar += self._empty_seq * (text_range - fill_index - 1)

        output = self.format.format(name=self.name,progress_bar=pbar,percentage=100*self.percentage)

        self.draw_text(self.get_first_col(),self.get_first_row(), output)
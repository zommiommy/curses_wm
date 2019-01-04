
import curses

from .window import Window

class ProgressBar(Window):

    def __init__(self,title:str = "", **kwargs):
        """Initialize the ProgressBar."""
        super().__init__(title, **kwargs)
        self.update_sequence = kwargs.get("update_sequence","0123456789#")
        self._empty_seq = kwargs.get("empty_seq","-")
        self.percentage : float = 0.0

    def set_update_sequence(self, sequence : str) -> None:
        """Set the sequence of symbols that the progrss bar will iterate from left to right. There MUST be at least 1 char"""
        if 1 > len(sequence):
            return
        self.update_sequence = sequence

    def set_empty_sequence(self, empty_seq : str) -> None:
        """Set the sequence for the empy part of the bar"""
        if len(empty_seq) < 1:
            return 
        self._empty_seq = empty_seq

    def set_percentage(self, percentage : float) -> None:
        """Set the percentage of complition, it must be a float between 0.0 and 1.0 """
        if percentage < 0:
            percentage = 0
        elif percentage > 1:
            percentage = 1
        self.percentage = percentage

    def _refresh_overriden(self) -> None:
        text_range = self.get_last_col() - self.get_first_col() + 1
        text_range *= len(self.update_sequence)

        index = int(text_range * self.percentage)

        fill_index = int(index / len(self.update_sequence))
        half_char = index % len(self.update_sequence)

        output = self.update_sequence[-1] * (fill_index)
        output += self.update_sequence[half_char]
        output += self._empty_seq * (self.get_last_col() - fill_index - 1)

        self.draw_text(self.get_first_col(),self.get_first_row(), output)
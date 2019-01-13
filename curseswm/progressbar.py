
import curses
from typing import Dict, Union

from .colours import *

class ProgressBar():

    styles = {
        "htop":{
            "update_sequence":"|",
            "empty_seq":" ",
            "format": "{name} [{progress_bar}{empty_bar}{percentage:.1f}%]"
        },
        "apt-get":{
            "update_sequence":"#",
            "empty_seq":"-",
            "format": "{name} [{percentage:.0f}%] [{progress_bar}{empty_bar}]"
        },
        "apt-get2":{
            "update_sequence":"0123456789#",
            "empty_seq":"-",
            "format": "{name} [{percentage:.0f}%] [{progress_bar}{empty_bar}]"
        },
        "pacman":{
            "update_sequence":"#",
            "empty_seq":"-",
            "format": "{name} [{progress_bar}{empty_bar}] {percentage:.0f}%"
        },
        "smooth":{
            "update_sequence": " ▏▎▍▌▋▊▉█",
            "empty_seq":" ",
            "format": "{name} | {percentage:.1f}% | {progress_bar}{empty_bar}>"
        },
        "equal":{
            "update_sequence": "=",
            "empty_seq":".",
            "format": "{name} [{progress_bar}>{percentage:.1f}%{empty_bar}]"
        }
    }

    def __init__(self,name:str = "", **kwargs):
        """ProgressBar(
            name: str,
            style: str,
            update_sequence: str,
            empty_seq: str,
            format: str)
        the format, empty_seq and update_sequence will be inherited from the default or chosen style if not specified."""
        self.name = name
        self.percentage : float = 0.0

        # Style setting
        self.style = self.styles[kwargs.get("style","smooth")]
        # Style expansion
        self.update_sequence = kwargs.get("update_sequence",self.style["update_sequence"])
        self.empty_seq = kwargs.get("empty_seq",self.style["empty_seq"])
        self.format = kwargs.get("format",self.style["format"])

    def __call__(self, percentage : float, str_len : int) -> str:
        if percentage < 0:
            percentage = 0
        elif percentage > 1:
            percentage = 1
        self.percentage = percentage
        self.str_len = str_len
        return self.__str__()

    def  __str__(self) -> str:
        # Calculate the total space for the bar
        text_range = self.str_len + 1

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

        return output
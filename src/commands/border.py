from enum import auto, Enum
from typing import Iterable
from utils.all_spaces import all_spaces
from commands.command import Command

class BorderStyle(Enum):
    NORMAL = auto()
    PIXEL = auto()
    TOGGLE = auto()
    ONE_PIXEL = auto()
    NONE = auto()

    @staticmethod
    def from_string(s: str):
        if s.lower() == "1pixel":
            return BorderStyle.ONE_PIXEL
        else:
            return BorderStyle[s.upper()]
    
    def __str__(self):
        if self.name.lower() == "one_pixel":
            return "1pixel"
        else:
            return self.name.lower()

class BorderArgument(object):
    def __init__(self, border_style: BorderStyle, value: int = None, spacing: Iterable[str] = all_spaces):
        self.border_style = border_style
        self.value = value
        self.spacing = spacing
    
    def __str__(self):
        spacing_iterator = iter(self.spacing)
        s = f"{str(self.border_style)}"
        if self.value:
            s += next(spacing_iterator)
            s += str(self.value)
        return s


class BorderCommand(Command):
    def __init__(self, border_argument: BorderArgument, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.border_argument = border_argument
        self.spacing = spacing

    def __str__(self):
        spacing_iterator = iter(self.spacing)
        return f"border{next(spacing_iterator)}{str(self.border_argument)}"
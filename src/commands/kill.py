from enum import Enum, auto
from typing import Iterable
from utils.enums import LowercaseEnum
from utils.all_spaces import all_spaces
from commands.command import Command


class KillTarget(LowercaseEnum):
    NONE = auto()
    WINDOW = auto()
    CLIENT = auto()

class KillCommand(Command):
    def __init__(self, target: KillTarget, spacing: Iterable[str] = all_spaces):
        self.target = target
        self.spacing = spacing

    def __str__(self):
        s = "kill"
        if self.target.value != KillTarget.NONE.value:
            s += self.spacing[0]
            s += str(self.target) 
        return s

from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Tuple, Iterable
from utils.all_spaces import all_spaces
from utils.measurement import Measurement
from utils.enums import *
from commands.command import Command

class I3MoveTarget(Enum):
    CONTAINER = auto()
    WINDOW = auto()
    TO = auto()
    NO_AUTO_BACK_AND_FORTH = auto()
    
    def __str__(self):
        if self.value == I3MoveTarget.CONTAINER.value:
            return "container"
        elif self.value == I3MoveTarget.WINDOW.value:
            return "window"
        elif self.value == I3MoveTarget.TO.value:
            return "to"
        elif self.value == I3MoveTarget.NO_AUTO_BACK_AND_FORTH.value:
            return "--no-auto-back-and-forth"

class I3MoveDestination(LowercaseEnum):
    OUTPUT = auto()
    MARK = auto()
    WORKSPACE = auto()
    POSITION = auto()

class I3MovePositionKind(LowercaseEnum):
    CENTER = auto()
    MOUSE = auto()
    CURSOR = auto()
    POINTER = auto()
    MEASUREMENT_PAIR = auto()

class I3MovePosition(object):
    def __init__(self, kind: I3MovePositionKind, data: Tuple = None):
        if kind == I3MovePositionKind.MEASUREMENT_PAIR:
            if data == None:
                raise ValueError("Cannot create an I3MovePosition of kind MEASUREMENT_PAIR with no data")
            elif len(data) != 3:
                raise ValueError(f"MEASUREMENT_PAIR data must have len() = 3 (Measurement, spacing, Measurement). Got len = {len(self.data)}")
        else:
            if data != None:
                raise ValueError(f"I3MovePosition of kind {kind} shouldn't use data. Data is only for MEASUREMENT_PAIR")

        self.kind = kind
        self.data = data
    
    def __str__(self):
        if self.kind.value != I3MovePositionKind.MEASUREMENT_PAIR.value:
            return self.kind.name.lower()
        else:
            x = self.data[0]
            space = self.data[1]
            y = self.data[2]
            return f"{str(x)}{space}{str(y)}"

class MoveCommand(Command):
    def __init__(self):
        super().__init__()
        self.move_targets = [] 
    
    def __str__(self) -> str:
        s = 'move'
        for space, target in zip(self.spacing, self.move_targets):
            s += space
            s += str(target)
        return s

    def _spaces_used_by_targets(self) -> int:
        """
        Returns the number of spaces used by self.move_targets
        """
        return len(self.move_targets)


class MoveWorkspace(MoveCommand):
    def __init__(self, destination: str, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.destination = destination
        self.spacing = spacing
    
    def __str__(self):
        spacing_start = self._spaces_used_by_targets()
        s = super().__str__()
        s += self.spacing[spacing_start]
        s += "workspace"
        s += self.spacing[spacing_start + 1]
        s += self.destination
        return s

class MoveWorkspaceTo(MoveCommand):
    def __init__(self, output_name: str, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.output_name = output_name
        self.spacing = spacing
    
    def __str__(self):
        spacing_start = self._spaces_used_by_targets()
        s = super().__str__()
        s += self.spacing[spacing_start]
        s += "workspace"
        s += self.spacing[spacing_start + 1]
        s += "to"
        s += self.spacing[spacing_start + 2]
        s += "output"
        s += self.spacing[spacing_start + 3]
        s += self.output_name
        return s

class MoveToOutput(MoveCommand):
    def __init__(self, output_name: str, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.output_name = output_name
        self.spacing = spacing

    def __str__(self):
        spacing_start = self._spaces_used_by_targets()
        s = super().__str__()
        s += self.spacing[spacing_start]
        s += "output"
        s += self.spacing[spacing_start + 1]
        s += self.output_name
        return s

class MoveToMark(MoveCommand):
    def __init__(self, mark_name: str, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.mark_name = mark_name
        self.spacing = spacing

    def __str__(self):
        spacing_start = self._spaces_used_by_targets()
        s = super().__str__()
        s += self.spacing[spacing_start]
        s += "mark"
        s += self.spacing[spacing_start + 1]
        s += self.mark_name
        return s
    
class MoveDirection(MoveCommand):
    def __init__(self, direction: Direction, measurement: Measurement = None, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.direction = direction
        self.measurement = measurement
        self.spacing = spacing
    
    def __str__(self):
        spacing_start = self._spaces_used_by_targets()
        s = super().__str__()
        s += self.spacing[spacing_start]
        s += str(self.direction)
        if self.measurement:
            s += self.spacing[spacing_start + 1]
            s += str(self.measurement)
        return s

    
class MoveToPosition(MoveCommand):
    def __init__(self, position: I3MovePosition, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.position = position
        self.spacing = spacing

    def __str__(self):
        spacing_start = self._spaces_used_by_targets()
        s = super().__str__()
        s += self.spacing[spacing_start]
        s += "position"
        s += self.spacing[spacing_start + 1]
        s += str(self.position)
        return s

class MoveToAbsolutePosition(MoveCommand):
    def __init__(self, position: I3MovePosition, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.position = position
        self.spacing = spacing

    def __str__(self):
        spacing_start = self._spaces_used_by_targets()
        s = super().__str__()
        s += self.spacing[spacing_start]
        s += "absolute"
        s += self.spacing[spacing_start + 1]
        s += "position"
        s += self.spacing[spacing_start + 2]
        s += str(self.position)
        return s

from enum import auto
from typing import Iterable
from utils.all_spaces import all_spaces
from utils.enums import LowercaseEnum
from utils.measurement import Measurement
from commands.command import Command

class ResizeRelativeKind(LowercaseEnum):
    SHRINK = auto()
    GROW = auto()

class ResizeDirection(LowercaseEnum):
    LEFT = auto()
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    WIDTH = auto()
    HEIGHT = auto()


class ResizeCommand(Command):
    def __init__(self):
        super().__init__()


class ResizeRelative(ResizeCommand):
    def __init__(self, relative_kind: ResizeRelativeKind, direction: ResizeDirection, pixel_measurement: Measurement = None, percentage_measurement: Measurement = None, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.relative_kind = relative_kind
        self.direction = direction
        self.pixel_measurement = pixel_measurement
        self.percentage_measurement = percentage_measurement
        self.spacing = spacing
    
    def __str__(self):
        spacing_iterator = iter(self.spacing)
        s = "resize"
        s += next(spacing_iterator)
        s += str(self.relative_kind)
        s += next(spacing_iterator)
        s += str(self.direction)
        if self.pixel_measurement:
            s += next(spacing_iterator)
            s += str(self.pixel_measurement)
            if self.percentage_measurement:
                s += next(spacing_iterator)
                s += "or"
                s += next(spacing_iterator)
                s += str(self.percentage_measurement)
        
        return s


class ResizeAbsolute(ResizeCommand):
    def __init__(self, width_explicit: bool = False, width_measurement: Measurement = None, height_explicit: bool = False, height_measurement: Measurement = None, spacing: Iterable[str] = all_spaces):
        super().__init__()
        # Can't have "resize set width" without a measurement
        if width_explicit:
            assert width_measurement
        
        # Can't have "resize set height" without a measurement
        if height_explicit:
            assert height_measurement

        # You can't do "resize set 10" and expect the 10 to be height
        if height_measurement and not width_measurement:
            assert height_explicit

        # Can't have "resize set" with nothing specified
        assert width_measurement or height_measurement

        self.width_explicit = width_explicit
        self.width_measurement = width_measurement
        self.height_explicit = height_explicit
        self.height_measurement = height_measurement
        self.spacing = spacing
    
    def __str__(self):
        spacing_iterator = iter(self.spacing)
        s = "resize"
        s += next(spacing_iterator)
        s += "set"
        if self.width_explicit:
            s += next(spacing_iterator)
            s += "width"
        if self.width_measurement:
            s += next(spacing_iterator)
            s += str(self.width_measurement)
        if self.height_explicit:
            s += next(spacing_iterator)
            s += "height"
        if self.height_measurement:
            s += next(spacing_iterator)
            s += str(self.height_measurement)
        return s

        
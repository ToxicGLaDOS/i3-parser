from typing import Iterable
from utils.enums import Unit

class Measurement(object):
    def __init__(self, number: int, unit: Unit = Unit.NONE, spacing: Iterable = ['']):
        self.number = number
        self.units = unit
        self.spacing = spacing
    
    def __str__(self):
        return f"{self.number}{next(iter(self.spacing))}{self.units}"
from enum import Enum, auto

class LowercaseEnum(Enum):
    @classmethod
    def from_string(cls, s: str):
        return cls[s.upper()]
    
    def __str__(self):
        return self.name.lower()

class NoneEnum(LowercaseEnum):
    @classmethod
    def from_string(cls, s: str):
        if s == "" or s == None:
            return cls["NONE"]
        else:
            return super().from_string(s)

    def __str__(self):
        if self.name == "NONE":
            return ""
        else:
            return super().__str__()

class EnableDisableToggle(LowercaseEnum):
    ENABLE = auto()
    DISABLE = auto()
    TOGGLE = auto()

class Direction(Enum):
    LEFT = auto()
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    @staticmethod
    def from_string(direction: str):
        return Direction[direction.upper()]
    
    def __str__(self):
        return self.name.lower()

class Unit(Enum):
    NONE = auto()
    PX = auto()
    PPT = auto()
    @staticmethod
    def from_string(unit: str):
        if unit == '':
            return Unit.NONE
        elif unit == 'px':
            return Unit.PX
        elif unit == 'ppt':
            return Unit.PPT
        else:
            raise ValueError(f"Expected one of ('', 'px', 'ppt') found {unit}.")

    def __str__(self):
        if self.value == Unit.NONE.value:
            return ''
        elif self.value == Unit.PX.value:
            return 'px'
        elif self.value == Unit.PPT.value:
            return 'ppt'
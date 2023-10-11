from enum import Enum


class EventType(Enum):
    LEC = 1,
    TUT = 2,
    OTH = 3,
    LAB = 4

    def __str__(self):
        return self.name

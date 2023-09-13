from enum import Enum


class TimeBlockMapping(Enum):
    From9amTo11am = 0
    From11amTo1pm = 1
    From2pmTo4pm = 2
    FROM4pmTo6pm = 3


class DayMapping(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5

from dataclasses import dataclass


@dataclass
class USCP_Params:
    """
    course = # courses
    events = # events for course i
    """
    courses: int
    events: [int]
    days: int
    time_blocks: int
    rooms: int

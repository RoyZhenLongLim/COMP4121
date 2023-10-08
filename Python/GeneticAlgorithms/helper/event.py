from dataclasses import dataclass, field
from .eventType import EventType


@dataclass
class Event:
    # Properties of the event
    courseCode: str
    eventType: EventType
    durationInHours: int

    # Restrictions/Limitations of the event
    allowedDays: [int]
    allowedRooms: [int]
    allowedTimes: [int]

    # Where is the event scheduled at
    dayTimeRoom: (int, int, int) = field(init=False)

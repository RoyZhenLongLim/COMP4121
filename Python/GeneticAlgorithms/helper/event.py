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
    allowedTimes: [int]
    allowedRooms: [int]

    def __str__(self):
        return "{} {}".format(
            self.courseCode,
            self.eventType,
        )

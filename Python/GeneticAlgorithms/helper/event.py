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

    # Where is the event scheduled at
    dayTimeRoom: (int, int, int) = field(init=False)

    def __str__(self):
        return f""" {self.courseCode} {self.eventType}
            allowed days = {self.allowedDays}
            allowed rooms = {self.allowedRooms}
            allowed times = {self.allowedTimes}
        """

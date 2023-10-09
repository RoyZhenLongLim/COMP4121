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
        if self.dayTimeRoom:
            return "{} {}: Day {} Room {} Time {}".format(self.courseCode, self.eventType, self.dayTimeRoom[0], self.dayTimeRoom[1], self.dayTimeRoom[2])
        else:
            return f""" {self.courseCode} {self.eventType}
                allowed days = {self.allowedDays}
                allowed rooms = {self.allowedRooms}
                allowed times = {self.allowedTimes}
            """

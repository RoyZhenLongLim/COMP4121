from dataclasses import dataclass
from event_type import EventType


@dataclass
class Event:
    """
    Duration in hours
    """
    event_type: EventType
    duration: int

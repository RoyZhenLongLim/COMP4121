from dataclasses import dataclass
from event_type import EventType


@dataclass
class Event:
    event_type: EventType

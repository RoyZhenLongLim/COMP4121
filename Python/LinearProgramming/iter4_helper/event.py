from dataclasses import dataclass


@dataclass
class Event:
    event_type: str
    allowed_rooms: list[str]

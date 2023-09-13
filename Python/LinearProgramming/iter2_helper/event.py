from dataclasses import dataclass


@dataclass
class Event:
    allowed_rooms: list[str]
    event_type: str

    def __init__(self, allowed_rooms: list[str], event_type: str):
        self.allowed_rooms = allowed_rooms
        self.event_type = event_type

    def rooms_for_event(self) -> int:
        return len(self.allowed_rooms)

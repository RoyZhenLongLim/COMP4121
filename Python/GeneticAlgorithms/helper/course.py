from dataclasses import dataclass

from .event import Event


@dataclass
class Course:
    course_code: str
    events: [Event]

    def get_num_events(self) -> int:
        return len(self.events)

    def get_event_type(self, event_index: int) -> str:
        return self.events[event_index].event_type

    def print_course(self):
        """
        Prints the course outline
        """
        print(f'Course Code: {self.course_code}')
        for event in self.events:
            print(f"    Event {event.event_type} can be scheduled in Rooms: {event.allowed_rooms}")

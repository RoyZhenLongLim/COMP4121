from dataclasses import dataclass

from Python.LinearProgramming.iter2_helper.event import Event


@dataclass
class Course:
    course_code: str
    events: [Event]

    def get_num_events(self) -> int:
        return len(self.events)

    def get_event_type(self, event_index: int) -> str:
        return self.events[event_index].event_type

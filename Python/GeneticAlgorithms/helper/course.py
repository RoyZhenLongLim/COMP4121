from dataclasses import dataclass
from .event import Event


@dataclass
class Course:
    course_code: str
    events: [Event]

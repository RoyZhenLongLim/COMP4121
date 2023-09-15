from dataclasses import dataclass

from Python.LinearProgramming.iter2_helper.event import Event


@dataclass
class Course:
    course_code: str
    events: list[Event]

    def __init__(self, course_code: str, events: list[Event]):
        self.course_code = course_code
        self.events = events

    def get_size(self, days, time_blocks, rooms) -> int:
        """
        :return: How many variables are required to represent in linear programming
        """
        return len(self.events) * days * time_blocks * rooms

    def get_num_events(self) -> int:
        """
        :return: Number of events for the course
        """
        return len(self.events)

    def event_description(self, index) -> str:
        """
        :param index: index of the event
        :return: print out what event is occurring in the given format
        [course_code] [event_type] at [day] [time_block] in [room]
        """
        return "%s" % self.course_code

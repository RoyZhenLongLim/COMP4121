from dataclasses import dataclass

from Python.LinearProgramming.iter2_helper.event import Event


@dataclass
class Course:
    course_code: str
    events: list[Event]

    def __init__(self, course_code: str, events: list[Event]):
        self.course_code = course_code
        self.events = events

    def get_size(self, days, time_blocks) -> int:
        """
        Determines how many variables are required to represent in linear programming
        :param days:
        :param time_blocks:
        :return:
        """
        return sum(days * time_blocks * event.rooms_for_event() for event in self.events)

    def unique_rooms(self) -> [str]:
        """
        :return: return rooms used
        """
        return []

    def indicies(self, day, time, room) -> [int]:
        """
        :param day: int
        :param time: int
        :param room: str
        :return: array of indices for events scheduled at specified day, time and room
        """
        return []

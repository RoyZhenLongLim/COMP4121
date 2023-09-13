from dataclasses import dataclass

from Python.LinearProgramming.iter2_helper.event import Event


def indicies_day_time_room(day, time, room) -> [int]:
    """
    :return: array of indices for events scheduled at specified day, time and room
    """
    return []


@dataclass
class Course:
    course_code: str
    events: list[Event]

    def __init__(self, course_code: str, events: list[Event]):
        self.course_code = course_code
        self.events = events

    def create_indices(self, start):
        """
        Creates a unique index for each event / room / time block / day
        index starts fromm start and ends at end
        """

    def get_size(self, days, time_blocks, rooms) -> int:
        """
        Determines how many variables are required to represent in linear programming
        :param rooms:
        :param days:
        :param time_blocks:
        :return:
        """
        return len(self.events) * days * time_blocks * rooms

    def indices_day_time(self, day, time) -> [int]:
        """
        :return: array of indices for event scheduled at same day and time
        """
        return []

    def event_description(self, index) -> str:
        """
        :param index: index of the event
        :return: print out what event is occurring in the given format
        [course_code] [event_type] at [day] [time_block] in [room]
        """
        return "%s" % self.course_code

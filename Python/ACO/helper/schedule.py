from itertools import groupby
from math import log2
from .event import Event
from .eventType import EventType


def earlier(d1, t1, d2, t2) -> bool:
    """
    Returns if first event is earlier than second event
    """
    if d1 < d2:
        return True
    else:
        return t1 < t2


def day(d):
    match d:
        case 0:
            return "Monday"
        case 1:
            return "Tuesday"
        case 2:
            return "Wednesday"
        case 3:
            return "Thursday"
        case 4:
            return "Friday"


class Schedule:
    events: [Event]
    fitness: float
    starting_day_time_room: [(int, int, int)]

    fitness_evaluated = False
    is_valid_schedule = False

    def __init__(self, events_to_schedule: [Event]):
        self.events = events_to_schedule

    def __eval_fitness(self):
        # If all events are scheduled without conflict, set is_valid_schedule to true
        self.fitness = 0
        self.is_valid_schedule = True
        bonus = 0

        index = 0
        courses = [list(ele) for _, ele in groupby(self.events, lambda ele: ele.courseCode)]
        for course in courses:
            earliest_index = index
            for _ in course:
                # If any event is not scheduled, set is_valid_schedule to false, otherwise increment fitness
                if self.starting_day_time_room == (-1, -1, 1):
                    self.is_valid_schedule = False
                else:
                    self.fitness += 1

                (d1, t1, r1) = self.starting_day_time_room[index]
                (d2, t2, r2) = self.starting_day_time_room[earliest_index]

                if earlier(d1, t1, d2, t2):
                    earliest_index = index

                index += 1

            if self.events[earliest_index].eventType == EventType.LEC:
                bonus += 1

        self.fitness += log2(bonus)

    def __lt__(self, other):
        # If fitness has not been re-evaluated since last change, do so
        if not self.fitness_evaluated:
            self.__eval_fitness()
            self.fitness_evaluated = True
        return self.fitness > other.fitness

    def __str__(self):
        representation = "\n"
        for index, d, t, r in enumerate(self.starting_day_time_room):
            event = self.events[index]
            representation += f"    {event.courseCode} {event.eventType} {day(d)} Time {9 + t}-{9 + t + event.durationInHours} Room {r} \n"
        return representation

    def add_event_starting_day_time_room(self, d, t, r):
        self.fitness_evaluated = False
        self.starting_day_time_room.append((d, t, r))

    def export_event_day_time_room(self) -> [(int, int, int, int)]:
        """
        Returns all the time slots booked with their corresponding event in the format (event index, day, time, room)
        """
        arr = []
        for index, (d, t, r) in self.starting_day_time_room:
            for hour in self.events[index].durartionInHours:
                arr.append((index, d, t + hour, r))
            pass

        return arr

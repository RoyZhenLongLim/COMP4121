import random
from copy import copy
from typing import Optional
from itertools import groupby, combinations
from math import log2

from .eventType import EventType
from .scheduleMatrix import ScheduleMatrix
from .event import Event


def generate_day_time_room(days: [int], times: [int], rooms: [int]) -> (int, int, int):
    # Randomly select a day
    return (
        random.choice(days),
        random.choice(times),
        random.choice(rooms)
    )


def overlap(d1, t1, duration1, d2, t2, duration2) -> bool:
    """
    Check if two events are overlapping
    """
    if d1 is not d2:
        return False
    else:
        start1, end1 = t1, t1 + duration1
        start2, end2 = t2, t2 + duration2
        return not (start1 < start2 and end1 <= start2) or (start1 >= end2 and end1 > end2)


def earlier(d1, t1, d2, t2) -> bool:
    """
    Returns if first event is earlier than second event
    """
    if d1 < d2:
        return True
    else:
        return t1 < t2


def generate_mask(n: int, pts: [int]) -> [int]:
    """
    Returns a mask for crossovers
    """
    arr = []
    ele = True
    for index in range(n):
        if index in pts:
            ele = not ele
        arr.append(ele)
    return arr


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
    fitness = 1
    timetable: ScheduleMatrix
    events: [(Event, int, int, int)]

    # Parameters that can be tweaked
    mutation_probability = 1 / 3
    crossover_probability = 2 / 3
    mutation_size = 1
    crossover_points = 1

    def __init__(self, events: [Event], timetable: Optional[ScheduleMatrix] = None):
        if timetable is None:
            # Generate a new timetable
            self.timetable = ScheduleMatrix()
            self.events = []

            for index, event in enumerate(events):
                d, t, r = generate_day_time_room(event.allowedDays, event.allowedTimes, event.allowedRooms)
                self.timetable.insert_event(index, d, t, r, event.durationInHours)
                event.dayTimeRoom = (d, t, r)
                self.events.append((event, d, t, r))
        else:
            # If timetable was pre-generated, we can skip
            self.events = events
            self.timetable = timetable

        self.__compute_fitness()

    def mutate(self):
        if random.uniform(0, 1) < self.mutation_probability:
            return

        # Randomly selected mutation_size many elements to mutate
        toMutate = random.choices([index for index in range(len(self.events))], k=self.mutation_size)

        for index in toMutate:
            # Remove event from timetable
            event, d, t, r = self.events[index]
            self.timetable.remove_event(index, d, t, r, event.durationInHours)

            # Randomised when the event is scheduled and reinsert into the timetable
            d, t, r = generate_day_time_room(event.allowedDays, event.allowedTimes, event.allowedRooms)
            self.timetable.insert_event(index, d, t, r, event.durationInHours)
            self.events[index] = (event, d, t, r)

        self.__compute_fitness()

    def crossover(self, other):
        if random.uniform(0, 1) < self.crossover_probability:
            if random.uniform(0, 1) > 0.5:
                return copy(self)
            else:
                return copy(other)

        timetable = ScheduleMatrix()
        events = []

        mask = generate_mask(
            len(self.events),
            random.choices([ele for ele in range(len(self.events))], k=self.crossover_points)
        )

        # Perform crossover
        for index, (left, right) in enumerate(zip(self.events, other.events)):
            if mask[index]:
                (e, d, t, r) = copy(left)
            else:
                (e, d, t, r) = copy(right)
            events.append((e, d, t, r))
            timetable.insert_event(index, d, t, r, e.durationInHours)

        return Schedule(events, timetable)

    def __compute_fitness(self):
        fitness = 1
        # Hard Constraints
        # Check that no two events have overlapping day, time, room
        for e, d, t, r in self.events:
            hours = self.timetable.get_events(d, t, r, e.durationInHours)
            if any(len(events) > 1 for events in hours):
                continue
            # For each event that does not overlap with another event, add 1 to fitness
            fitness += 1

        # Check that no two events in the same course have the day, time with overlapping duration
        courses = [list(ele) for _, ele in groupby(self.events, lambda ele: list(ele)[0].courseCode)]

        for course in courses:
            for (e1, d1, t1, r1), (e2, d2, t2, r2) in combinations(course, r=2):
                if overlap(d1, t1, e1.durationInHours, d2, t2, e2.durationInHours):
                    fitness -= 1

        # If multiple lectures are scheduled on same day, reduce fitness by 1
        for course in courses:
            lec_per_day = [0] * 5
            for (e, d, t, r) in course:
                if e.eventType == EventType.LEC:
                    lec_per_day[d] += 1
            for lecs in lec_per_day:
                if lecs > 1:
                    fitness -= 1

        # Implement Soft Constraints
        # Soft constraint bonus only occurs when
        if fitness > len(self.events):
            bonus = 1
            # If the first event scheduled is a LEC, bonus points (this is to ensure
            for course in courses:
                (E, D, T, R) = course[0]
                for (e, d, t, r) in course:
                    if earlier(d, t, D, T):
                        (E, D, T, R) = (e, d, t, r)
                if E.eventType == EventType.LEC:
                    bonus += 1
            fitness += log2(bonus)

        self.fitness = fitness

    def __lt__(self, other):
        return self.fitness <= other.fitness

    def __str__(self):
        representation = "\n"
        for event, d, t, r in self.events:
            representation += f"    {event.courseCode} {event.eventType} {day(d)} Time {9 + t}-{9 + t + event.durationInHours} Room {r} \n"
        return representation

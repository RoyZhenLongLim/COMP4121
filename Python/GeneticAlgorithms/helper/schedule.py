import random
from typing import Optional

from .scheduleMatrix import ScheduleMatrix
from .event import Event


def generate_day_time_room(days: [int], times: [int], rooms: [int]) -> (int, int, int):
    # Randomly select a day
    return (
        random.choice(days),
        random.choice(times),
        random.choice(rooms)
    )

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


class Schedule:
    fitness = 1
    timetable: ScheduleMatrix
    events: [Event]

    # Parameters that can be tweaked
    mutation_probability = 1 / 3
    crossover_probability = 2 / 3
    mutation_size = 2
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
                self.events.append(event)
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
            d, t, r = self.events[index].dayTimeRoom
            event = self.events[index]
            self.timetable.remove_event(index, d, t, r, event.durationInHours)

            # Randomised when the event is scheduled and reinsert into the timetable
            d, t, r = generate_day_time_room(event.allowedDays, event.allowedTimes, event.allowedRooms)
            self.timetable.remove_event(index, d, t, r, event.durationInHours)
            self.events[index].dayTimeRoom = (d, t, r)

        self.__compute_fitness()

    def crossover(self, other):
        if random.uniform(0, 1) < self.crossover_probability:
            if random.uniform(0, 1) > 0.5:
                return self
            else:
                return other

        timetable = ScheduleMatrix()
        events = []

        mask = generate_mask(
            len(self.events),
            random.choices([ele for ele in range(len(events))], k=self.crossover_points)
        )

        # Perform crossover
        for index, left, right in enumerate(zip(self.events, other.events)):
            if mask[index]:
                e = left
            else:
                e = right
            events.append(e)
            d, t, r = e.DayTimeRoom
            timetable.insert_event(index, d, t, r, e.duration)

        return Schedule(events, timetable)

    def __compute_fitness(self):
        # TODO: Implement hard constraints
        # Hard Constraints
        # Check that no two events have overlapping day, time, room
        # Check that no two events in the same course have the day, time with overlapping duration
        self.fitness = random.randint(0, 5)

    def __lt__(self, other):
        return self.fitness <= other.fitness

    def __str__(self):
        # TODO Modify to show more information regarding the schedules
        return "Fitness: {}".format(self.fitness)

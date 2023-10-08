import random

from .scheduleMatrix import ScheduleMatrix
from .event import Event


def generate_day_time_room(allowedDays: [int], allowedTimes: [int], allowedRooms: [int]) -> (int, int, int):
    return (
        random.choices(allowedDays),
        random.choices(allowedTimes),
        random.choices(allowedRooms)
    )


class Schedule:
    fitness = 1
    timetable: ScheduleMatrix
    events: [Event]

    def __init__(self, events: [Event]):
        self.timetable = ScheduleMatrix()

        for index, event in enumerate(events):
            d, t, r = generate_day_time_room(event.allowedDays, event.allowedTimes, event.allowedRooms)
            self.timetable.insert_event(index, d, t, r, event.durationInHours)
            event.dayTimeRoom = (d, t, r)
            self.events.append(event)

        self.__compute_fitness()

    def mutate(self) -> None:
        self.__compute_fitness()

    def __compute_fitness(self):
        self.fitness = random.randint(0, 5)

    def __lt__(self, other):
        return self.fitness <= other.fitness

    def __str__(self):
        # TODO Modify to show more information regarding the schedules
        return "Fitness: {}".format(self.fitness)

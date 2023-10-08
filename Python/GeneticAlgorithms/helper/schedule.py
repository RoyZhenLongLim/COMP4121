import random

from .scheduleMatrix import ScheduleMatrix
from .event import Event

class Schedule:
    fitness = 1
    timetable: ScheduleMatrix

    def __init__(self, events: [Event]):
        self.timetable = ScheduleMatrix()
        for index, event in enumerate(events):
            d, t, r = 0, 0, 0
            self.timetable.insert_event(index, d, t, r, event.durationInHours)
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

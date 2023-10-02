import random


class Schedule:
    fitness = 1

    def __init__(self):
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

import random
import heapq as hq

from helper.course import Course
from helper.schedule import Schedule


class TimetableScheduler:
    population: [Schedule]

    # State Space
    days = 5
    hours_per_day = 12
    rooms = 2

    # Parameters that can be tweaked
    population_size = 10

    mutation_probability = 1 / 3
    mutation_size: int
    crossover_probability = 2 / 3
    crossover_points: int

    def __init__(self, courses: [Course]):
        # TODO FINISH THIS
        self.population = [Schedule() for _ in range(self.population_size)]

    def __crossover(self, parent1: Schedule, parent2: Schedule):
        # TODO CREATE CROSSOVER FUNCTION
        if random.uniform(0, 1) > 0.5:
            return parent1
        else:
            return parent2

    def __select_parents(self, breeding_pool, w):
        """
        Probability of being selected is proportional to fitness (i.e. weight given)
        :return: two parents from the breeding pool
        """
        return random.choices(breeding_pool, weights=w, k=2)

    def solve(self) -> Schedule:
        generation = 0
        while generation < 10:
            # Create breeding pool
            breeding_pool = self.population
            hq.heapify(breeding_pool)
            w = [s.fitness for s in breeding_pool]

            best_schedule = hq.nlargest(1, breeding_pool)[0]

            # Display the best solution in current generation
            print("Generation {}: ".format(generation), end="")
            print(best_schedule)
            generation = generation + 1

            # TODO FIX THIS
            criteria = 50
            if best_schedule.fitness >= criteria:
                return best_schedule

            # Create 2 * population_size / 3 new populations
            new_schedules = []
            for _ in range(int(2 * self.population_size / 3)):
                # Select two parents based on their fitness and create a child
                if random.uniform(0, 1) > self.crossover_probability:
                    p1, p2 = self.__select_parents(breeding_pool, w)
                    child = self.__crossover(p1, p2)
                else:
                    child = Schedule()

                #
                if random.uniform(0, 1) > self.mutation_probability:
                    child.mutate()

                new_schedules.append(child)

            hq.heapify(new_schedules)

            # Take the best solutions in current generation
            self.population = list(hq.nlargest(self.population_size, hq.merge(new_schedules, breeding_pool)))


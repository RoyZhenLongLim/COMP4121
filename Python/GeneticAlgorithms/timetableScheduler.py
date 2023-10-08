import random
import heapq as hq

from helper.event import Event
from helper.schedule import Schedule


class TimetableScheduler:
    population: [Schedule]

    # Parameters that can be tweaked
    population_size = 10

    mutation_probability = 1 / 3
    mutation_size = 2
    crossover_probability = 2 / 3
    crossover_points = 1

    def __init__(self, events: [Event]):
        # TODO FINISH INIT Function
        # TODO LOOK AT Parameters
        for e in events:
            print(e)

    def __crossover(self, parent1: Schedule, parent2: Schedule):
        # TODO CREATE CROSSOVER FUNCTION
        self.population_size = self.population_size
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
                p1, p2 = self.__select_parents(breeding_pool, w)
                if random.uniform(0, 1) > self.crossover_probability:
                    # Select two parents where probability of being chosen is proportional to fitness
                    child = self.__crossover(p1, p2)
                else:
                    # Otherwise, use the parents as a basis for new generation
                    if random.uniform(0, 1) > 0.5:
                        child = p1
                    else:
                        child = p2

                if random.uniform(0, 1) > self.mutation_probability:
                    child.mutate()

                new_schedules.append(child)

            hq.heapify(new_schedules)

            # Take the best solutions in current generation
            self.population = list(hq.nlargest(self.population_size, hq.merge(new_schedules, breeding_pool)))


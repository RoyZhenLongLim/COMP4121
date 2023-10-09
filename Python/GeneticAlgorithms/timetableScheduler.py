import random
import heapq as hq

from helper.event import Event
from helper.schedule import Schedule


class TimetableScheduler:
    population: [Schedule]

    # Parameters that can be tweaked
    population_size = 10

    def __init__(self, events: [Event]):
        # Create initial population
        self.population = []
        for _ in range(self.population_size):
            self.population.append(
                Schedule(events)
            )

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
                # Probability of being selected is proportional to fitness
                p1, p2 = random.choices(breeding_pool, weights=w, k=2)
                child = p1
                child = p1.crossover(p2)
                child.mutate()
                new_schedules.append(child)

            hq.heapify(new_schedules)

            # Take the best solutions in current generation
            self.population = list(hq.nlargest(self.population_size, hq.merge(new_schedules, breeding_pool)))

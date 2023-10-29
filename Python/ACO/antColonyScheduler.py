import numpy as np
from itertools import groupby

from helper.event import Event
from helper.schedule import Schedule


class AntColonyScheduler:
    n_ants: int
    n_best: int
    events: [Event]
    preference: [[int]]
    pheromones: [[float]]
    time_slots = [(int, int, int)]
    days: int
    time_blocks: int
    rooms: int

    # Tweak-able Parameters
    alpha = 1
    beta = 1
    evaporation_constant = 0.2
    tau_max = 10
    tau_min = 1

    def __init__(self, n_ants: int, n_best: int, events_to_schedule: [Event], days: int, time_blocks: int, rooms: int):
        self.n_ants = n_ants
        self.n_best = n_best
        self.events = events_to_schedule
        self.days = days
        self.time_blocks = time_blocks
        self.rooms = rooms

        self.preference = np.full((len(events_to_schedule), days, time_blocks, rooms), 0)
        self.pheromones = np.full((len(events_to_schedule), days, time_blocks, rooms), self.tau_max)

        # TODO FINISH THIS UP
        self.time_slots = np.array([

        ])
        # TODO COMPUTE PREFERENCE MATRIX

    def optimize(self) -> Schedule:
        best_schedule = self.generate_schedule()

        generation = 0
        countdown_started = False
        counter = 0

        while True:
            # For each iteration, generate schedule
            schedules = self.generate_schedules()
            schedules = sorted(schedules, reverse=True)

            # If new best schedule has been found, replace current solution
            if schedules[0] > best_schedule:
                best_schedule = schedules[0]
                # If countdown has started, restart it
                if countdown_started:
                    counter = max(generation / 4, 100)

            # Once we found the best solution, start a countdown to see if solution can be improved within a
            # fixed number of generations
            if not countdown_started and best_schedule.is_valid_schedule:
                countdown_started = True
                counter = max(generation / 4, 100)

            if countdown_started:
                counter -= 1
                if counter <= 0:
                    return best_schedule

            # Display the best solution in current generation
            print("Generation {}: Fitness: {}".format(generation, best_schedule.fitness), end="")
            print(best_schedule)
            generation = generation + 1

            self.evaporate_pheromone()
            for s in schedules[:self.n_best]:
                self.spread_pheromone(s)

    def evaporate_pheromone(self):
        # Pheromone is volatile and will evaporate over time
        self.pheromones = self.pheromones * (1 - self.evaporation_constant)
        # Pheromone cannot go below a minimum ensure that stopping at local minima
        self.pheromones[self.pheromones < self.tau_min] = self.tau_min

    def spread_pheromone(self, s: Schedule):
        # Pheromone smooth Delta Tau is proportional to tau_max - tau
        # Delta Tau = (tau_max - tau) / n_best
        # The more ants there are, the less effective the pheromone of one ant is
        pass

    def generate_schedules(self) -> [Schedule]:
        return [self.generate_schedule() for _ in range(self.n_ants)]

    def generate_schedule(self) -> Schedule:
        s = Schedule(self.events)
        # GROUP COURSES BY COURSE CODE
        taken = []

        index = 0
        # Group courses by their course code
        courses = [list(ele) for _, ele in groupby(self.events, lambda ele: ele.courseCode)]
        for course in courses:
            course_conflicts = []
            for event in course:
                (d, t, r) = self.generate_day_time_room(self.preference[index], self.pheromones[index], [], [])
                for hour in event.durationInHours:
                    taken.append((d, t + hour, r))
                    course_conflicts.append((d, t + hour))
                # TODO: Add to schedule
            index += 1
        return s

    def generate_day_time_room(self, available_slots, pheromones, already_taken: (int, int, int),
                               course_conflict: (int, int)) -> (int, int, int):
        pher = np.copy(pheromones)
        pref = np.copy(available_slots)
        # Do not schedule in any time slot that has already been taken
        pher[already_taken] = 0
        # Do not schedule in any time slot if an event from the same course is already scheduled
        for (d, t) in course_conflict:
            pher[(d, t)] = 0
        # Convert from 3D matrix to 1D array
        pher = np.reshape(pher, -1)
        pref = np.reshape(pref, -1)
        # Compute probability for each time slot to be chosen
        prob = pher ** self.alpha * pref ** self.beta
        prob = prob / np.sum(prob)
        # Choose a time_slot
        return np.random.choice(self.time_slots, p=prob)

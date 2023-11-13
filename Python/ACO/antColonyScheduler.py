import numpy as np
from itertools import groupby

from helper.eventType import EventType
from helper.event import Event
from helper.schedule import Schedule


class AntColonyScheduler:
    n_ants: int
    n_best: int
    events: [Event]
    preference: [[int]]
    pheromones: [[float]]
    time_slots: [(int, int, int)]
    time_slot_index: [int]
    days: int
    time_blocks: int
    rooms: int

    # Tweak-able Parameters
    alpha = 1
    beta = 1
    evaporation_constant = 0.2
    tau_max = 10
    tau_min = 1

    default_preference = 10

    def __init__(self, n_ants: int, n_best: int, events_to_schedule: [Event], days: int, time_blocks: int, rooms: int):
        self.n_ants = n_ants
        self.n_best = n_best
        self.events = events_to_schedule
        self.days = days
        self.time_blocks = time_blocks
        self.rooms = rooms

        self.preference = np.full((len(events_to_schedule), days, time_blocks, rooms), 0)
        self.pheromones = np.full((len(events_to_schedule), days, time_blocks, rooms), self.tau_max)

        self.time_slots = np.array([
            (d, t, r)
            for d in range(days)
            for t in range(time_blocks)
            for r in range(rooms)
        ])
        self.time_slot_index = np.array([i for i in range(days * time_blocks * rooms)])

        for index, event in enumerate(events_to_schedule):
            for d in event.allowedDays:
                for t in event.allowedTimes:
                    for r in event.allowedRooms:
                        self.preference[(index, d, t, r)] = self.default_preference

    def optimize(self) -> Schedule:
        best_schedule = self.generate_schedule()
        max_iteration = 1
        for t in range(max_iteration):
            schedules = self.generate_schedules()
            schedules = sorted(schedules, reverse=True)

            # If new best schedule has been found, replace current solution
            if schedules[0] > best_schedule:
                best_schedule = schedules[0]

            # Display the best solution in current generation
            print("Generation {}: Fitness: {}".format(t, best_schedule.fitness), end="\n")

            # Pheromone are volatile and evaporate over time,
            self.evaporate_pheromone()

            # The ants with the best path will spread their pheromones
            for s in schedules[:self.n_best]:
                self.spread_pheromone(s)

        return best_schedule

    def evaporate_pheromone(self):
        # Pheromone is volatile and will evaporate over time
        self.pheromones = self.pheromones * (1 - self.evaporation_constant)
        # Pheromone cannot go below a minimum ensure that stopping at local minima
        self.pheromones[self.pheromones < self.tau_min] = self.tau_min

    def spread_pheromone(self, s: Schedule):
        # Pheromone smoothing => change in pheromone is proportional to difference between current pheromone and max
        # The more ants there are, the less effective the pheromone of one ant is
        for pheromone_trail in s.export_event_day_time_room():
            self.pheromones[pheromone_trail] = (self.tau_max - self.pheromones[pheromone_trail]) / self.n_best

    def generate_schedules(self) -> [Schedule]:
        return [self.generate_schedule() for _ in range(self.n_ants)]

    def generate_schedule(self) -> Schedule:
        s = Schedule(self.events)
        already_taken = []
        index = 0
        # Group courses by their course code
        courses = [list(ele) for _, ele in groupby(self.events, lambda ele: ele.courseCode)]
        for course in courses:
            course_conflicts = []
            for event in course:
                (d, t, r) = self.generate_day_time_room(
                    event,
                    self.preference[index],
                    self.pheromones[index],
                    already_taken,
                    course_conflicts
                )

                for hour in range(event.durationInHours):
                    already_taken.append((d, t + hour, r))
                    course_conflicts.append((event.eventType, d, t + hour))
                s.add_event_starting_day_time_room(d, t, r)
                index += 1
        return s

    def generate_day_time_room(self,
                               event: Event,
                               available_slots: [[[int]]],
                               pheromones: [[[int]]],
                               already_taken: [(int, int, int)],
                               course_conflict: [(EventType, int, int)]) -> (int, int, int):
        pher = np.copy(pheromones)
        pref = np.copy(available_slots)
        # Do not schedule in any time slot that has already been taken
        for taken in already_taken:
            pher[taken] = 0

        # Do not schedule in any time slot if an event from the same course is already scheduled
        for (_, d, t) in course_conflict:
            pher[(d, t)] = 0
            print(f"Course Conflict: {d, t}")

        # Do not schedule multiple lectures on the same day
        if event.eventType == EventType.LEC:
            for (type, d, _) in course_conflict:
                if type == EventType.LEC:
                    pher[d] = 0

        # Convert from 3D matrix to 1D array
        pher = np.reshape(pher, -1)
        pref = np.reshape(pref, -1)
        # Compute probability for each time slot to be chosen
        prob = (pher ** self.alpha) * (pref ** self.beta)

        if np.sum(prob) == 0:
            # If there are no available time slots, return -1 for each
            return -1, -1, -1
        prob = prob / np.sum(prob)
        # Choose a time_slot
        index = np.random.choice(self.time_slot_index, p=prob)
        return self.time_slots[index]

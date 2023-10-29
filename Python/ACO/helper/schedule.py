from .event import Event


class Schedule:
    events: [Event]
    fitness: float
    starting_day_time_room: [(int, int, int)]

    fitness_evaluated = False
    is_valid_schedule = False

    def __init__(self, events_to_schedule: [Event]):
        self.events = events_to_schedule

    def __eval_fitness(self):
        # If all events are scheduled without conflict, set is_valid_schedule to true
        self.fitness = 1

    def __lt__(self, other):
        # If fitness has not been re-evaluated since last change, do so
        if not self.fitness_evaluated:
            self.__eval_fitness()
            self.fitness_evaluated = True
        return self.fitness > other.fitness

    def __str__(self):
        # TODO DO THIS
        return ""

    def add_event_starting_day_time_room(self, d, t, r):
        self.starting_day_time_room.append((d, t, r))

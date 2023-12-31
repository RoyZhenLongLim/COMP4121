import time
import random
from statistics import mean, stdev

from helper.config import config
from helper.eventType import EventType
from helper.event import Event
from passwordGuesser import PasswordGuesser
from geneticScheduler import GeneticScheduler


def generate_day_time_room(days: [int], times: [int], rooms: [int]) -> (int, int, int):
    # Randomly select a day
    return (
        random.choice(days),
        random.choice(times),
        random.choice(rooms)
    )


def benchmark(fun, n_repeat: int):
    run_time = []
    for n in range(n_repeat):
        start = time.time()
        fun()
        end = time.time()
        run_time.append(end - start)

    mu = mean(run_time)
    sigma = stdev(run_time)
    print("Mean: {:.3f}, Standard Deviation: {:.3f}".format(mu, sigma))


def main():
    # Generates test data
    # LEC must be in room 1
    # TUT, OTH must be in room 2
    # Note events can't be scheduled at the end of the day (e.g. a 2 hours event can't be scheduled
    events = []
    for i in range(1, 3):
        events.extend([
            Event(
                f"PHYS11{i}1",
                EventType.LEC,
                2,
                [ele for ele in range(config["days"])],
                [ele for ele in range(config["timeBlocks"] - 2 + 1)],
                [ele for ele in [0, 1, 2, 3]]
            ),
            Event(
                f"PHYS11{i}1",
                EventType.LEC,
                2,
                [ele for ele in range(config["days"])],
                [ele for ele in range(config["timeBlocks"] - 2 + 1)],
                [ele for ele in [0, 1, 2, 3]]
            ),
            Event(
                f"PHYS11{i}1",
                EventType.OTH,
                2,
                [ele for ele in range(config["days"])],
                [ele for ele in range(config["timeBlocks"] - 2 + 1)],
                [ele for ele in [4, 5, 6]]
            ),
            Event(
                f"PHYS11{i}1",
                EventType.LAB,
                2,
                [ele for ele in range(config["days"])],
                [ele for ele in range(config["timeBlocks"] - 2 + 1)],
                [ele for ele in [4, 5, 6]]
            ),
        ])

    s = GeneticScheduler(events)
    # s.solve()
    g = PasswordGuesser("Hello World")
    g.guess()


if __name__ == "__main__":
    main()

import time
import random
from statistics import mean, stdev

from helper.config import config
from helper.eventType import EventType
from helper.event import Event
from timetableScheduler import TimetableScheduler


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
    events.extend([
        Event(
            f"PHYS1111",
            EventType.LEC,
            2,
            [ele for ele in range(config["days"])],
            [ele for ele in range(config["timeBlocks"] - 2 + 1)],
            [ele for ele in [0]]
        ),
        Event(
            f"PHYS1111",
            EventType.LEC,
            2,
            [ele for ele in range(config["days"])],
            [ele for ele in range(config["timeBlocks"] - 2 + 1)],
            [ele for ele in [0]]
        ),
        Event(
            f"PHYS1111",
            EventType.OTH,
            2,
            [ele for ele in range(config["days"])],
            [ele for ele in range(config["timeBlocks"] - 2 + 1)],
            [ele for ele in [1]]
        ),
        Event(
            f"PHYS1111",
            EventType.LAB,
            2,
            [ele for ele in range(config["days"])],
            [ele for ele in range(config["timeBlocks"] - 2 + 1)],
            [ele for ele in [1]]
        ),
    ])

    # from itertools import groupby, combinations
    # arr = [(e, index, index, index) for index, e in enumerate(events)]
    #
    # lst = [list(g) for _, g in groupby(arr, lambda ele: list(ele)[0].courseCode)]
    #
    # for (e1, d1, t1, r1), (e2, d2, t2, r2) in combinations(lst[0], r=2):
    #     print(e1, e2)

    s = TimetableScheduler(events)
    s.solve()


if __name__ == "__main__":
    main()

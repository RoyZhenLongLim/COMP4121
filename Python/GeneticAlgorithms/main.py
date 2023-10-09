import time
from statistics import mean, stdev

from helper.config import config
from helper.eventType import EventType
from helper.event import Event
from timetableScheduler import TimetableScheduler


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
    for index in range(1, 2):
        events.extend([
            Event(
                f"PHYS11{index}1",
                EventType.LEC,
                2,
                [ele for ele in range(config["days"])],
                [ele for ele in range(config["timeBlocks"] - 2 + 1)],
                [ele for ele in [1]]
            ),
            Event(
                f"PHYS11{index}1",
                EventType.LEC,
                2,
                [ele for ele in range(config["days"])],
                [ele for ele in range(config["timeBlocks"] - 2)],
                [ele for ele in [1]]
            ),
            Event(
                f"PHYS11{index}1",
                EventType.OTH,
                2,
                [ele for ele in range(config["days"])],
                [ele for ele in range(config["timeBlocks"] - 2)],
                [ele for ele in [2]]
            ),
            Event(
                f"PHYS11{index}1",
                EventType.LAB,
                2,
                [ele for ele in range(config["days"])],
                [ele for ele in range(config["timeBlocks"] - 2)],
                [ele for ele in [2]]
            ),

        ])

    s = TimetableScheduler(events)
    s.solve()


if __name__ == "__main__":
    main()

import time
from statistics import mean, stdev

from helper.event_type import EventType
from helper.course import Course
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
    data = [
        Course(
            "PHYS1111",
            [
                Event(EventType.LEC, 2),
                Event(EventType.LEC, 2),
                Event(EventType.LAB, 2),
                Event(EventType.OTH, 2),
            ]
        ),
    ]

    s = TimetableScheduler([])
    s.solve()


if __name__ == "__main__":
    main()

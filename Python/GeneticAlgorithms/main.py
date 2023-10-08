import time
from statistics import mean, stdev

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
    s = TimetableScheduler()
    s.solve()


if __name__ == "__main__":
    main()

import random
import time
from statistics import mean, stdev

from guesser import Guesser
from passwordGuesser import PasswordGuesser


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
    def f():
        # Randomly generate a 10 integer long target, where each integer are in [0, 50)
        limit = 50
        target = random.sample(range(limit), 10)
        guesser = Guesser(target, limit)
        # guesser.set_verbose(False)
        guesser.solve()

    # def f():
    #     g = PasswordGuesser("Hello World Hello Hwllo")
    #     g.guess()
    f()
    # benchmark(f, 50)


if __name__ == "__main__":
    main()

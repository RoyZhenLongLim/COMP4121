import time
from statistics import mean, stdev

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
    # Gives a password that the guesser will try to guess using genetic algorithms
    def run_guesser():
        password = "Hello World! This is my first attempt at creating a genetic algorithm"
        guesser = PasswordGuesser(password)
        guesser.set_verbose(False)
        guesser.guess()

    benchmark(
        run_guesser,
        50
    )


if __name__ == "__main__":
    main()

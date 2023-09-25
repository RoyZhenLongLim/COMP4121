import time

from passwordGuesser import PasswordGuesser


def benchmark(fun):
    start = time.time()
    fun()
    end = time.time()
    print(f"Function took {end - start:.3f} seconds to complete")


def main():
    # Gives a password that the guesser will try to guess using genetic algorithms
    password = "Hello World! This is my first attempt at creating a genetic algorithm"
    guesser = PasswordGuesser(password)
    benchmark(
        guesser.guess
    )


if __name__ == "__main__":
    main()

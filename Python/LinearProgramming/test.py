class test:
    counter = 1


def main():
    print(test.counter)

    def incr(i):
        i += 1

    incr(test.counter)
    print(test.counter)


if __name__ == "__main__":
    main()

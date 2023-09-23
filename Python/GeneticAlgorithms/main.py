from helper.course import Course
from helper.event import Event
from algorithm import Algorithm


def main():
    courses = [
        Course("PHYS1111",
               [
                   Event("LEC", [0]),
                   Event("LEC", [0]),
                   Event("OTH", [1]),
                   Event("LAB", [2]),
               ]),
        Course("PHYS1121",
               [
                   Event("LEC", [0]),
                   Event("LEC", [0]),
                   Event("OTH", [1]),
                   Event("LAB", [2]),
               ]),
        Course("PHYS1131",
               [
                   Event("LEC", [0]),
                   Event("LEC", [0]),
                   Event("OTH", [1]),
                   Event("LAB", [2]),
               ])
    ]
    ga = Algorithm(courses)


if __name__ == "__main__":
    main()

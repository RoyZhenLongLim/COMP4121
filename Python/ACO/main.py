from Python.ACO.antColonyScheduler import AntColonyScheduler
from aco import AntColony
from helper.event import Event
from helper.eventType import EventType


def main():
    # Generates test data
    # LEC must be in room 1
    # TUT, OTH must be in room 2
    # Note events can't be scheduled at the end of the day (e.g. a 2 hours event can't be scheduled
    config = {
        "days": 5,
        "timeBlocks": 9,
        "rooms": 7
    }

    events = []
    for i in range(1, 4):
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
    n_ants = 4
    n_best = 2
    scheduler = AntColonyScheduler(
        n_ants,
        n_best,
        events,
        config["days"],
        config["timeBlocks"],
        config["rooms"],
    )

    s = scheduler.optimize()


if __name__ == "__main__":
    main()

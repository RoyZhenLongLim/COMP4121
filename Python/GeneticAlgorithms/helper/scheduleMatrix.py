from .config import config


class ScheduleMatrix:
    matrix: [[[int]]]

    def __init__(self):
        self.matrix = [
            [
                [
                    [] for _ in range(config["rooms"])
                ] for _ in range(config["timeBlocks"])
            ] for _ in range(config["days"])
        ]

    def insert_event(self, event_index: int, day: int, time: int, room: int, duration: int):
        for hour in range(duration):
            self.matrix[day][time + hour][room].append(event_index)

    def remove_event(self, event_index: int, day: int, time: int, room: int, duration: int):
        for hour in range(duration):
            self.matrix[day][time + hour][room].remove(event_index)

    def get_events(self, day: int, time: int, room: int, duration: int) -> [[int]]:
        """
        E.g. day = 1, time = 1, room = 1, duration = 2 => [[1], [2]]
        Event 1 is scheduled at Monday 9am in Room 1
        Event 2 is scheduled at Monday 10am in Room 1

        :param day:
        :param time:
        :param room:
        :param duration: in hours
        :return: Array of events schedule at the day, time, room and duration
        """
        arr = []
        for hour in range(duration):
            arr.append(self.matrix[day][time + hour][room])
        return arr

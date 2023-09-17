import random
from dataclasses import dataclass, field


@dataclass
class USCP_Params:
    """
    course = # courses
    events = # events for course i
    """
    courses: int
    events: [int]
    days: int
    time_blocks: int
    rooms: int
    random_map: [int] = field(init=False)

    def __post_init__(self):
        arr = [i for i in range(sum(event for event in self.events) * self.days * self.time_blocks * self.rooms)]
        random.shuffle(arr)
        self.random_map = arr

    def random_index(self, index):
        return self.random_map[index]

from dataclasses import dataclass


@dataclass
class USCP_Params:
    events: int
    days: int
    time_blocks: int
    rooms: int

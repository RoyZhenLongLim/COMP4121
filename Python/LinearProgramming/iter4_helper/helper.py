def generate_event_description(course_code: str, event_type: str, day: int, time: int, room: int) -> str:
    day_map = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
    }

    time_map = {
        0: '9am - 11am',
        1: '11am - 1pm',
        2: '2pm - 4pm',
        3: '4pm - 6pm'
    }
    string = f"Event {course_code} {event_type} is in room {room} on {day_map[day]} {time_map[time]}"
    return string


def compute_index(config, course, event, day, time, room):
    # Randomised index means it generates a schedule for you
    return config.random_index(
        course * (config.events[course] * config.days * config.time_blocks * config.rooms) + \
        event * (config.days * config.time_blocks * config.rooms) + \
        day * (config.time_blocks * config.rooms) + \
        time * config.rooms + \
        room
    )

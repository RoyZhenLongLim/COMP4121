from ortools.linear_solver import pywraplp

from Python.LinearProgramming.iter2_helper.course import Event, Course


class LP2:
    days = 2
    time_blocks = 2  # Morning and Afternoon
    room_map = ["A", "B"]
    rooms = 2
    courses = [
        Course("PHYS1111",
               [
                   Event(["A"], "LEC"),
                   Event(["B"], "TUT")
               ])
    ]

    # Defaults for data
    data = {
        "constraint_coeffs": [],
        "bounds": [],
        "obj_coeffs": [],
        "num_vars": -1,
        "num_constraints": -1
    }

    def __constraint_day_time_room(self, day, time, room) -> [int]:
        """
        :return: an array of indices for all events at day, time and room
        """
        arr = []

        for i, course in enumerate(self.courses):
            for j, event in enumerate(course.events):
                arr.append(
                    i * (course.get_num_events() * self.days * self.time_blocks * self.rooms) +
                    j * (self.days * self.time_blocks * self.rooms) +
                    day * (self.time_blocks * self.rooms) +
                    time * self.rooms +
                    room
                )

        return arr

    def __constraint_same_course(self, course_index, course, day, time) -> [int]:
        """
        :return: an array of indices for all events
        """
        arr = []
        for event_index in range(course.get_num_events()):
            for room in range(self.rooms):
                arr.append(
                    course_index * (course.get_num_events() * self.days * self.time_blocks * self.rooms) +
                    event_index * (self.days * self.time_blocks * self.rooms) +
                    day * (self.time_blocks * self.rooms) +
                    time * self.rooms +
                    room
                )
        return arr

    def __generate_constraint_arr(self, constraint_indices: [int]) -> [int]:
        arr = [0] * self.data['num_vars']
        for index in constraint_indices:
            arr[index] = 1
        return arr

    def __init__(self):
        """
        Initialise data to be solved
        """
        self.data["num_vars"] = sum(course.get_size(self.days, self.time_blocks, self.rooms) for course in self.courses)

        self.events = sum(course.get_num_events() for course in self.courses)

        # For each day, for each time block, for each room, there can only be 1 event scheduled in that room
        for day in range(self.days):
            for time in range(self.time_blocks):
                for room in range(self.rooms):
                    self.data['constraint_coeffs'].append(
                        self.__generate_constraint_arr(
                            self.__constraint_day_time_room(day, time, room)
                        )
                    )
                    self.data['bounds'].append(1)

        # For each course, no two events can be scheduled on the same day, at the same time
        for index, course in enumerate(self.courses):
            for day in range(self.days):
                for time in range(self.time_blocks):
                    self.data['constraint_coeffs'].append(
                        self.__generate_constraint_arr(
                            self.__constraint_same_course(index, course, day, time)
                        )
                    )
                    self.data['bounds'].append(1)

        # Each event is only allocated once
        for course_index, course in enumerate(self.courses):
            for event_index, event in enumerate(course.events):
                start = course_index * (course.get_num_events() * self.days * self.time_blocks * self.rooms) + \
                        event_index * (self.days * self.time_blocks * self.rooms)
                end = start + self.days * self.time_blocks * self.rooms

                self.data['constraint_coeffs'].append(
                    self.__generate_constraint_arr(
                        [1 if (index >= start & index < end) else 0 for index in range(self.data['num_vars'])]
                    )
                )
                self.data['bounds'].append(1)

        # Restriction on rooms each event can be in
        # TODO:

        self.data["obj_coeffs"] = [1] * (self.days * self.time_blocks * self.rooms * self.events)
        self.data["num_constraints"] = len(self.data["constraint_coeffs"])

        # ? Generate an array that stores all the event indices?

        for constraint in self.data['constraint_coeffs']:
            print(constraint)

    def solve(self):
        # Creating the solver
        solver = pywraplp.Solver.CreateSolver("SCIP")
        if not solver:
            return

        x = {}
        for j in range(self.data["num_vars"]):
            # TODO: Make this use proper names, i.e. PHYS2111 Lecture at Time X in Room Y
            x[j] = solver.BoolVar('%d' % j)
            # Include as a phantom variable (always set to 0)
            # x[j] = solver.IntVar(0, 0, '%d' % j)

        # Create constraints
        for i in range(self.data['num_constraints']):
            constraint_expr = \
                [self.data['constraint_coeffs'][i][j] * x[j] for j in range(self.data['num_vars'])]
            solver.Add(sum(constraint_expr) <= self.data['bounds'][i])

        # Defining objective function
        obj_expr = [self.data['obj_coeffs'][j] * x[j] for j in range(self.data['num_vars'])]
        solver.Maximize(solver.Sum(obj_expr))

        # Solve and Output solution
        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            print("Objective value =", solver.Objective().Value())
            for j in range(self.data["num_vars"]):
                print(x[j].name(), " = ", x[j].solution_value())
            print()
            print("Problem solved in %f milliseconds" % solver.wall_time())
            print("Problem solved in %d iterations" % solver.iterations())
            print("Problem solved in %d branch-and-bound nodes" % solver.nodes())
        else:
            print("The problem does not have an optimal solution.")


def main():
    algorithm = LP2()
    algorithm.solve()
    return 0


if __name__ == "__main__":
    main()

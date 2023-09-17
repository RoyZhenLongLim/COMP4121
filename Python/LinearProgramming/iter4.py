from ortools.linear_solver import pywraplp

from Python.LinearProgramming.iter4_helper.USCP_Params import USCP_Params
from Python.LinearProgramming.iter4_helper.course import Course
from Python.LinearProgramming.iter4_helper.event import Event
from Python.LinearProgramming.iter4_helper.helper import compute_index, generate_event_description


class LP4:
    def __init__(self):
        pass

    def solve(self):
        input = [
            Course("PHYS1111",
                   [
                       Event("LEC", ["A"]),
                       Event("TUT", ["B"]),
                   ]),
            Course("PHYS1211",
                   [
                       Event("LEC", ["A"]),
                       Event("TUT", ["B"]),
                   ])
        ]

        courses = len(input)
        events = [course.get_num_events() for course in input]
        days = 2
        time_blocks = 2
        rooms = 2

        config = USCP_Params(
            courses,
            events,
            days,
            time_blocks,
            rooms
        )

        data = {}
        data['num_vars'] = sum(course.get_num_events() for course in input) * days * time_blocks * rooms
        data['obj_coeffs'] = [1] * data['num_vars']

        # Create the mip solver with the SCIP backend.
        solver = pywraplp.Solver.CreateSolver("SCIP")
        if not solver:
            return

        # Initialising variables as binary integers
        x = {}
        for course in range(courses):
            for event in range(events[course]):
                for day in range(days):
                    for time in range(time_blocks):
                        for room in range(rooms):
                            index = compute_index(config, course, event, day, time, room)
                            x[index] = solver.BoolVar(
                                generate_event_description(
                                    input[course].course_code,
                                    input[course].get_event_type(event),
                                    day,
                                    time,
                                    room
                                )
                            )
        print("Number of variables =", solver.NumVariables())

        # creating constraints
        data['constraint_coeffs'] = []
        data['bounds'] = []

        # 1) at any day, time_block and room, there can only be 1 event
        # 2) each event is scheduled a maximum of once
        # 3) not event from each course can be scheduled at any same time

        data['num_constraints'] = len(data['constraint_coeffs'])

        # for i in range(data["num_constraints"]):
        #     constraint = solver.RowConstraint(0, data["bounds"][i], "")
        #     for j in range(data["num_vars"]):
        #         constraint.SetCoefficient(x[j], data["constraint_coeffs"][i][j])
        # print("Number of constraints =", solver.NumConstraints())

        # Create Objective Function
        objective = solver.Objective()
        for j in range(data["num_vars"]):
            objective.SetCoefficient(x[j], data["obj_coeffs"][j])
        objective.SetMaximization()

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            print("Objective value =", solver.Objective().Value())
            for j in range(data["num_vars"]):
                print(x[j].name(), " = ", x[j].solution_value())
            print()
            print("Problem solved in %f milliseconds" % solver.wall_time())
            print("Problem solved in %d iterations" % solver.iterations())
            print("Problem solved in %d branch-and-bound nodes" % solver.nodes())
        else:
            print("The problem does not have an optimal solution.")


def main():
    algorithm = LP4()
    algorithm.solve()
    return 0


if __name__ == "__main__":
    main()

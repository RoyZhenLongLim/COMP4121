from ortools.linear_solver import pywraplp

from Python.LinearProgramming.iter4_helper.USCP_Params import USCP_Params
from Python.LinearProgramming.iter4_helper.course import Course
from Python.LinearProgramming.iter4_helper.event import Event
from Python.LinearProgramming.iter4_helper.helper import compute_index, generate_event_description


class LP5:
    def __init__(self):
        pass

    def solve(self):
        input = [
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

        courses = len(input)
        events = [course.get_num_events() for course in input]
        days = 5
        time_blocks = 2
        rooms = 3

        # Prints course that need to be scheduled
        for course in input:
            course.print_course()
        print()

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
                            if room not in input[course].events[event].allowed_rooms:
                                x[index] = solver.IntVar(
                                    0,
                                    0,
                                    generate_event_description(
                                        input[course].course_code,
                                        input[course].get_event_type(event),
                                        day,
                                        time,
                                        room
                                    ))
                            else:
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
        for day in range(days):
            for time in range(time_blocks):
                for room in range(rooms):
                    arr = [0] * data['num_vars']
                    for course in range(courses):
                        for event in range(events[course]):
                            index = compute_index(config, course, event, day, time, room)
                            arr[index] = 1
                    data['constraint_coeffs'].append(arr)
                    data['bounds'].append(1)

        # 2) each event is scheduled a maximum of once
        for course in range(courses):
            for event in range(events[course]):
                arr = [0] * data['num_vars']
                for day in range(days):
                    for time in range(time_blocks):
                        for room in range(rooms):
                            index = compute_index(config, course, event, day, time, room)
                            arr[index] = 1
                data['constraint_coeffs'].append(arr)
                data['bounds'].append(1)

        # 3) for any course, at most one event is scheduled at any given time
        for course in range(courses):
            for day in range(days):
                for time in range(time_blocks):
                    arr = [0] * data['num_vars']
                    for event in range(events[course]):
                        for room in range(rooms):
                            index = compute_index(config, course, event, day, time, room)
                            arr[index] = 1
                    data['constraint_coeffs'].append(arr)
                    data['bounds'].append(1)

        # 4) All lectures scheduled in the morning are prioritised (specifically in 9am-11am and 11am-1pm block)
        for course in range(courses):
            for event in range(events[course]):
                for day in range(days):
                    for time in range(time_blocks):
                        if time < 2 & (input[course].get_event_type(event) == "LEC"):
                            for room in range(rooms):
                                index = compute_index(config, course, event, day, time, room)
                                data['obj_coeffs'][index] *= 1.5
                        else:
                            continue

        # 5) Not more than one lecture per course per day
        for course in range(courses):
            lectures = []
            for event in range(events[course]):
                if input[course].get_event_type(event) == "LEC":
                    lectures.append(event)
            # At this point we have all the lectures / per
            for day in range(days):
                arr = [0] * data['num_vars']
                for lecture in lectures:
                    for time in range(time_blocks):
                        for room in range(rooms):
                            index = compute_index(config, course, lecture, day, time, room)
                            arr[index] = 1
                data['constraint_coeffs'].append(arr)
                data['bounds'].append(1)



        data['num_constraints'] = len(data['constraint_coeffs'])

        for i in range(data["num_constraints"]):
            constraint = solver.RowConstraint(0, data["bounds"][i], "")
            for j in range(data["num_vars"]):
                constraint.SetCoefficient(x[j], data["constraint_coeffs"][i][j])
        print("Number of constraints =", solver.NumConstraints())

        # Create Objective Function
        objective = solver.Objective()
        for j in range(data["num_vars"]):
            objective.SetCoefficient(x[j], data["obj_coeffs"][j])
        objective.SetMaximization()

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            print("Objective value =", solver.Objective().Value())
            soln = []
            for j in range(data["num_vars"]):
                if x[j].solution_value() == 1:
                    soln.append(x[j].name())
            soln.sort()
            for e in soln:
                print(e)

            print()
            print("Problem solved in %f milliseconds" % solver.wall_time())
            print("Problem solved in %d iterations" % solver.iterations())
            print("Problem solved in %d branch-and-bound nodes" % solver.nodes())
        else:
            print("The problem does not have an optimal solution.")


def main():
    algorithm = LP5()
    algorithm.solve()
    return 0


if __name__ == "__main__":
    main()

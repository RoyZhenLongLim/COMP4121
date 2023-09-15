from ortools.linear_solver import pywraplp

from Python.LinearProgramming.iter3_helper.USCP_Params import USCP_Params


class LP3:
    def __init__(self):
        pass

    def __compute_index(self, params: USCP_Params, day, time, room, event):
        index = event * (params.days * params.time_blocks * params.rooms) + \
                day * (params.time_blocks * params.rooms) + \
                time * params.rooms + \
                room
        return index

    def __generate_event_description(self, day, time, room, event):
        day_map = {
            0: 'Monday',
            1: 'Tuesday',
        }

        time_map = {
            0: 'Morning',
            1: 'Afternoon'
        }
        string = f"Event {event} is in room {room} on {day_map[day]} {time_map[time]}"
        return string

    def solve(self):
        # Default Params
        days = 2  # Day 0, 1
        time_blocks = 2  # Morning, Afternoon
        rooms = 2  # Room 0, 1
        events = 5  # LEC, TUT

        data = {}
        data['num_vars'] = events * days * time_blocks * rooms
        data['obj_coeffs'] = [1] * data['num_vars']

        # Create the mip solver with the SCIP backend.
        solver = pywraplp.Solver.CreateSolver("SCIP")
        if not solver:
            return

        # Initialising variables as binary integers
        x = {}
        for day in range(days):
            for time in range(time_blocks):
                for room in range(rooms):
                    for event in range(events):
                        index = self.__compute_index(
                            USCP_Params(events, days, time_blocks, rooms),
                            day,
                            time,
                            room,
                            event)
                        x[index] = solver.BoolVar(
                            self.__generate_event_description(day, time, room, event)
                        )

        print("Number of variables =", solver.NumVariables())

        # Creating constraints
        data['constraint_coeffs'] = []
        data['bounds'] = []

        # 1) at any day, time_block and room, there can only be 1 event
        for day in range(days):
            for time in range(time_blocks):
                for room in range(rooms):
                    arr = [0] * data['num_vars']
                    for event in range(events):
                        index = self.__compute_index(
                            USCP_Params(events, days, time_blocks, rooms),
                            day,
                            time,
                            room,
                            event)
                        arr[index] = 1
                    data['constraint_coeffs'].append(arr)
                    data['bounds'].append(1)
        # 2) each event is scheduled a maximum of once
        for event in range(events):
            arr = [0] * data['num_vars']
            for day in range(days):
                for time in range(time_blocks):
                    for room in range(rooms):
                        index = self.__compute_index(
                            USCP_Params(events, days, time_blocks, rooms),
                            day,
                            time,
                            room,
                            event)
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
            for j in range(data["num_vars"]):
                if x[j].solution_value() == 1:
                    print(x[j].name(), " = ", x[j].solution_value())
            print()
            print("Problem solved in %f milliseconds" % solver.wall_time())
            print("Problem solved in %d iterations" % solver.iterations())
            print("Problem solved in %d branch-and-bound nodes" % solver.nodes())
        else:
            print("The problem does not have an optimal solution.")


def main():
    algorithm = LP3()
    algorithm.solve()
    return 0


if __name__ == "__main__":
    main()

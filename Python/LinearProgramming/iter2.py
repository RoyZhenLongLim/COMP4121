from ortools.linear_solver import pywraplp

from Python.LinearProgramming.iter2_helper.course import Event, Course


class LP2:
    days = 1
    time_blocks = 4
    counter = 0
    rooms = ["A", "B", "C"]

    # Defaults for data
    data = {
        "constraint_coeffs": [
            [5, 7, 9, 2, 1],
            [18, 4, -9, 10, 12],
            [4, 7, 3, 8, 5],
            [5, 13, 16, 3, -7],
        ],
        "bounds": [20, 20, 20, 20],
        "obj_coeffs": [7, 8, 2, 9, 6],
        "num_vars": 5,
        "num_constraints": 4
    }

    def __init__(self):
        """
        Initialise data to be solved
        """
        courses = [
            Course("PHYS1111",
                   [
                       Event(["A"], "LEC"),
                       Event(["A"], "LEC"),
                       Event(["B"], "LAB"),
                       Event(["C"], "OTH")
                   ])
        ]
        self.data["num_vars"] = sum(course.get_size(self.days, self.time_blocks, len(self.rooms)) for course in courses)
        print(self.data["num_vars"])

        # TODO: Ensure that each room at each time slot on each day can only be booked once
        # TODO: Ensure that for each course, there are no overlapping events

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
    # algorithm.solve()
    return 0


if __name__ == "__main__":
    main()

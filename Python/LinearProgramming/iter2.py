from ortools.linear_solver import pywraplp
from enum import Enum

from Python.LinearProgramming.iter2_helper.course import Event, Course


class TimeBlockMapping(Enum):
    From9amTo11am = 0
    From11amTo1pm = 1
    From2pmTo4pm = 2
    FROM4pmTo6pm = 3


class DayMapping(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5


class LP2:
    days = 1
    time_blocks = 4

    # Defaults for data
    data = {
        "constraint_coeffs": [
            [5, 7, 9, 2, 1],
            [18, 4, -9, 10, 12],
            [4, 7, 3, 8, 5],
            [5, 13, 16, 3, -7],
        ],
        "bounds": [250, 285, 211, 315],
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
        # self.data['num_vars'] = sum(course.get_size(self.days, self.time_blocks) for course in courses)

    def solve(self):
        # Creating the solver
        solver = pywraplp.Solver.CreateSolver("SCIP")
        if not solver:
            return

        x = {}
        for j in range(self.data["num_vars"]):
            # TODO: Make this use proper names, i.e. PHYS2111 Lecture at Time X in Room Y
            x[j] = solver.BoolVar('%d' % j)

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

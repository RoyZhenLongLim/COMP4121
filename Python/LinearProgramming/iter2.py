from ortools.linear_solver import pywraplp


class LP2:
    days = 2

    def __init__(self):
        pass

    def solve(self):
        solver = pywraplp.Solver.CreateSolver("GLOP")
        if not solver:
            return
        x = solver.BoolVar('x')
        y = solver.BoolVar('y')

        print("Number of variables =", solver.NumVariables())

        # Constraint 0: x + 2y <= 14.
        solver.Add(x + 2 * y <= 14.0)

        # Constraint 1: 3x - y >= 0.
        solver.Add(3 * x - y >= 0.0)

        # Constraint 2: x - y <= 2.
        solver.Add(x - y <= 2.0)

        print("Number of constraints =", solver.NumConstraints())

        # Objective function: 3x + 4y.
        solver.Maximize(3 * x + 4 * y)

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            print("Solution:")
            print("Objective value =", solver.Objective().Value())
            print("x =", x.solution_value())
            print("y =", y.solution_value())
        else:
            print("The problem does not have an optimal solution.")

    def add_constraint(self):
        pass


def main():
    algorithm = LP2()
    algorithm.add_constraint()
    algorithm.solve()
    return 0


if __name__ == "__main__":
    main()

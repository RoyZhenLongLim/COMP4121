from ortools.linear_solver import pywraplp


class LP1:
    data = {}

    def __init__(self):
        """
            init produces a schedule (1 day, 4 sessions, 4 events of 2 hours in length and schedules them)
            Constraints should be done automatically
            Room availability should be considered
            Scheduling for multiple days should also be included
        """
        events = 4
        days = 1
        sessions = 4

        n = events * days * sessions

        self.data["num_vars"] = events * days * sessions

        # Create constraint such that each does not exceed 1
        self.data["constraint_coeffs"] = []
        self.data["bounds"] = []

        def binary_constraint(length, index):
            return [ele == index for ele in range(length)]

        for i in range(self.data["num_vars"]):
            self.data["constraint_coeffs"].append(binary_constraint(n, i))
            self.data["bounds"].append(1)

        # Ensure that each session can have at most 1 event occurring at that time
        def events_cant_overlap_constraint(length, sessions):
            for i in range(sessions):
                arr = [0] * length
                j = i
                while (j < length):
                    arr[j] = 1
                    j += sessions
                self.data["constraint_coeffs"].append(arr)
                self.data["bounds"].append(1)

        events_cant_overlap_constraint(n, sessions)

        # Each event has to be scheduled exactly once
        for event in range(events):
            arr = [0] * n
            for i in range(event * sessions, event * sessions + sessions):
                arr[i] = 1
            self.data["constraint_coeffs"].append(arr)
            self.data["bounds"].append(1)

        self.data["num_constraints"] = len(self.data["constraint_coeffs"])
        self.data["obj_coeffs"] = [1] * n

    def solve(self):
        solver = pywraplp.Solver.CreateSolver("SCIP")
        if not solver:
            return

        infinity = solver.infinity()

        x = {}
        for j in range(self.data["num_vars"]):
            x[j] = solver.IntVar(0, infinity, "x[%i]" % j)
        print("Number of variables =", solver.NumVariables())

        for i in range(self.data["num_constraints"]):
            constraint = solver.RowConstraint(0, self.data["bounds"][i], "")
            for j in range(self.data["num_vars"]):
                constraint.SetCoefficient(x[j], self.data["constraint_coeffs"][i][j])
        print("Number of constraints =", solver.NumConstraints())

        objective = solver.Objective()
        for j in range(self.data["num_vars"]):
            objective.SetCoefficient(x[j], self.data["obj_coeffs"][j])
        objective.SetMaximization()

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
    lp_iter1 = LP1()
    lp_iter1.solve()


if __name__ == "__main__":
    main()

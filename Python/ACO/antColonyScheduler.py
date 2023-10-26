class AntColonyScheduler:
    n_ants: int
    n_best: int

    # Tweak-able Parameters
    alpha = 1
    beta = 1
    evaporation_constant = 0.2
    max_iterations = 5000
    Q = 4

    def __init__(self, n_ants, n_best):
        self.n_ants = n_ants
        self.n_best = n_best

    def optimize(self):
        pass

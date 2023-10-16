import random


class TravelingSalesman:
    # Parameters
    alpha = 0.5
    beta = 0.8
    Q = 80
    tau_max = 2

    # Data Structure
    adjacency_matrix: [[int]]
    pheromones: [[int]]
    delta_pheromones: [[int]]

    def __init__(self, nAnts: int, nCities: int):
        self.adjacency_matrix = [[0] * nCities] * nCities
        self.pheromones = [[0] * nCities] * nCities
        self.delta_pheromones = [[0] * nCities] * nCities

    def connect_cities(self, i: int, j: int) -> None:
        # Connect the two cities
        self.adjacency_matrix[i][j] = 1
        self.adjacency_matrix[j][i] = 1

        # Create pheromones
        self.pheromones[i][j] = random.uniform(0, 1) * self.tau_max
        self.pheromones[j][i] = random.uniform(0, 1) * self.tau_max

    def optimize(self, max_iterations):
        for iteration in max_iterations:
            pass

        # TODO Print Results

    def print_graph(self) -> None:
        # PRINT Graph Representation
        print("Graph")

    def print_pheromones(self) -> None:
        # Print Pheromone Representation
        print("Pheromones")

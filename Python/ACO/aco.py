import numpy as np


class AntColony:
    n_vertices: int
    n_ants: int
    n_best: int
    adjacency_matrix: [[int]]
    pheromones: [[float]]

    # Tweak-able Parameters
    alpha = 1
    beta = 1
    evaporation_constant = 0.2
    max_iterations = 5000
    Q = 4

    def __init__(self, n_vertices, n_ants, n_best):
        self.n_vertices = n_vertices
        self.n_ants = n_ants
        self.n_best = n_best
        self.adjacency_matrix = np.full((n_vertices, n_vertices), np.inf)
        self.pheromones = np.full((n_vertices, n_vertices), 1)

    def add_edge(self, i, j, weight):
        """
        Adds an edge between vertex i and j
        """
        self.adjacency_matrix[i][j] = weight
        self.adjacency_matrix[j][i] = weight

    def optimize(self) -> (str, float):
        all_time_shortest_path = ("placeholder", np.inf)
        for t in range(self.max_iterations):
            all_paths = self.gen_all_paths()
            # Pheromones from previous generation evaporates slightly
            self.pheromones = self.pheromones * (1 - self.evaporation_constant)
            # New pheromone from this iteration is spread
            self.spread_pheromones(all_paths)
            shortest_path = min(all_paths, key=lambda x: x[1])
            # If new shortest path is found, update
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path

        return all_time_shortest_path

    def spread_pheromones(self, all_paths: [[(int, int)]]):
        """
        Spread pheromone on the path traversed by the n_best ants
        """
        paths = sorted(all_paths, key=lambda x: x[1])[:self.n_best]
        for path, path_len in paths:
            for (a, b) in path:
                self.pheromones[a][b] += self.Q / self.adjacency_matrix[a][b]
                self.pheromones[b][a] += self.Q / self.adjacency_matrix[b][a]

    def gen_all_paths(self) -> [[(int, int)]]:
        """
        For each ant, generate a random cycle depending on current pheromone levels and return it
        """
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start: int) -> [(int, int)]:
        """
        Generates a Hamiltonian Cycle for a specific ant
        """
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(self.n_vertices - 1):
            move = self.pick_move(self.pheromones[prev], self.adjacency_matrix[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))
        return path

    def gen_path_dist(self, path: [(int, int)]) -> int:
        """
        Returns the path length of a given path
        """
        path_length = 0
        for a, b in path:
            path_length += self.adjacency_matrix[a][b]
        return path_length

    def pick_move(self, pheromones: [float], distances: [int], visited: set[int]) -> int:
        """
        Given pheromones and distance, randomly select a vertex to move to that hasn't been visited before
        """
        prob = np.copy(pheromones)
        prob[list(visited)] = 0

        prob = prob ** self.alpha * ((1 / distances) ** self.beta)
        prob = prob / np.sum(prob)

        move = np.random.choice([i for i in range(self.n_vertices)], p=prob)

        return move

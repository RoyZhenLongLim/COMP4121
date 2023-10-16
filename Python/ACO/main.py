from .travelingSalesman import TravelingSalesman


def main():
    ants = 4
    cities = 8
    max_iterations = 200
    ts = TravelingSalesman(ants, cities)
    connections = [
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 7),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 4),
        (2, 5),
        (2, 6),
        (4, 3),
        (4, 5),
        (4, 7),
        (6, 7),
    ]

    for city_i, city_j in connections:
        ts.connect_cities(city_i, city_j)

    ts.print_graph()
    ts.print_pheromones()
    ts.optimize(max_iterations)


if __name__ == "__main__":
    main()

from aco import AntColony


def main():
    n_vertices = 4
    n_ants = 1
    n_best = 1
    edges = [
        (0, 1, 1),
        (1, 2, 1),
        (2, 3, 1),
        (3, 0, 1),
    ]

    aco = AntColony(n_vertices, n_ants, n_best)

    for i, j, weights in edges:
        aco.add_edge(i, j, weights)

    print(
        aco.optimize()
    )


if __name__ == "__main__":
    main()

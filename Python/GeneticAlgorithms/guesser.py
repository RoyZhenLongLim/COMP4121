import random


class Guesser:
    target: [int]
    gene_set: [int]
    limit: int
    population = []

    # Default Parameters
    n_population = 5
    mutation_probability = 1 / 3
    verbose = True
    # Ensure Results are consistent and replicable
    random.seed(0)

    def __init__(self, target: [int], limit: int):
        self.target = target
        self.limit = limit
        self.population = []

        # Initialise default population
        self.population = [random.sample(range(self.limit), len(target)) for _ in range(self.n_population)]

    def set_verbose(self, b: bool):
        self.verbose = b

    def __mutate(self, child: [int]):
        """Chose an arbitrary index to mutate"""
        if random.uniform(0, 1) < self.mutation_probability:
            # A random index is now changed to something not seen in the set
            newInt = random.randint(0, self.limit - 1)
            while newInt in child:
                newInt = random.randint(0, self.limit - 1)
            child[random.randint(0, len(self.target) - 1)] = newInt
        return child

    def __crossover(self, parent1: [int], parent2: [int]) -> [int]:
        child = []
        gene_set = set(parent1) | set(parent2)
        for gene1, gene2 in zip(parent1, parent2):
            inChild1, inChild2 = (gene1 in child), (gene2 in child)
            # if neither gene are already in the child, select one at random
            if inChild1 and inChild2:
                if random.uniform(0, 1) >= 5:
                    child.append(gene1)
                else:
                    child.append(gene2)
            # if both are in the child, generate a random gene not found in gene_set of either parent
            elif (not inChild1) and (not inChild2):
                newInt = random.randint(0, self.limit - 1)
                while newInt in gene_set:
                    newInt = random.randint(0, self.limit - 1)
                child.append(newInt)
            elif not inChild1:
                child.append(gene1)
            elif not inChild2:
                child.append(gene2)
        return child

    def __select_parents(self, breeding_pool, w):
        """
        Probability of being selected is proportional to fitness (i.e. weight given)
        :return: two parents from the breeding pool
        """
        p1, p2 = random.choices(breeding_pool, weights=w, k=2)
        return p1["population"], p2["population"]

    def __fitness_check(self, curr: [int]) -> int:
        """
        Start from 0, how many of the integers are strictly ascending
        Every element in curr must be unique
        :return: fitness of solution
        """
        fitness = 1
        for i in range(len(curr) - 1):
            if curr[i] < curr[i + 1]:
                fitness = fitness + 1
            else:
                break
        return fitness

    def __display(self, n_generation, best_soln, fitness):
        if self.verbose:
            print("Generation {}: best solution is {} with a fitness of {}".format(n_generation, best_soln, fitness))

    def solve(self):
        generation = 0
        while True:
            # Create a breeding pool
            breeding_pool = []
            for index, pop in enumerate(self.population):
                pop_characteristics = {
                    "fitness": self.__fitness_check(pop),
                    "population": pop
                }
                breeding_pool.append(pop_characteristics)

            # Sort based on fitness and extract the one with the highest fitness
            breeding_pool = sorted(breeding_pool, key=lambda ele: ele["fitness"])
            best_pop = breeding_pool[-1]["population"]
            best_fitness = breeding_pool[-1]["fitness"]

            # Print the population number and highest fitness solution of the new generation
            self.__display(generation, best_pop, best_fitness)
            generation = generation + 1

            # Check if it passes the criteria
            # Every integer in the list is an ascending integer
            criteria = len(self.target)
            if best_fitness >= criteria:
                return best_pop

            # Create a new population set
            # Returns the top third of the old population to ensure that population does regress in fitness
            new_population = []
            for fitness_rating in breeding_pool[-int(self.n_population / 3):]:
                new_population.append(fitness_rating.__getitem__("population"))

            # Probability of being selected as a parent is proportional to fitness
            weights = [pop["fitness"] for pop in breeding_pool]
            while len(new_population) <= self.n_population:
                # Randomly chose two parents and create a child then mutate it
                parent1, parent2 = self.__select_parents(breeding_pool, weights)
                child = self.__crossover(parent1, parent2)
                child = self.__mutate(child)
                new_population.append(child)

            self.population = new_population

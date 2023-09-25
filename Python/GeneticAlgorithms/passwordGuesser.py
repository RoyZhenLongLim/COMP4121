import random


class PasswordGuesser:
    password: str
    verbose: bool
    geneSet = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!."

    def __init__(self, password: str):
        self.password = password
        random.seed()

    def set_verbose(self, b: bool):
        self.verbose = b

    def guess(self):
        bestParent = self.__generate_parent(len(self.password))
        bestFitness = self.__get_fitness(bestParent)

        while True:
            child = self.__mutate(bestParent)
            childFitness = self.__get_fitness(child)

            # If child is less fit than the best previous option, ignore it
            if childFitness <= bestFitness:
                continue

            if self.verbose:
                self.__display(child)
            # If I guessed correctly, exit loop
            if childFitness >= len(bestParent):
                break

            bestFitness = childFitness
            bestParent = child

    def __generate_parent(self, length: int) -> str:
        """
        Generate unique starting genes with as many unique genes are possible
        """
        genes = []
        while len(genes) < length:
            sampleSize = min(length - len(genes), len(self.geneSet))
            genes.extend(random.sample(self.geneSet, sampleSize))

        return ''.join(genes)

    def __get_fitness(self, guess: str) -> int:
        """
        :param guess:
        :return: How many characters match the original
        """
        return sum(1 for expected, actual in zip(self.password, guess) if expected == actual)

    def __mutate(self, parent):
        index = random.randrange(0, len(parent))
        childGenes = list(parent)
        newGene, alternative = random.sample(self.geneSet, 2)
        # Change the gene at index to either alternative or newGene
        childGenes[index] = alternative \
            if newGene == childGenes[index] \
            else newGene
        return ''.join(childGenes)

    def __display(self, guess):
        fitness = self.__get_fitness(guess)
        print(f"Guess: {guess}\t Fitness: {fitness}")

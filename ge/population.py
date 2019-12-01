""" Population class """
import random
from spacy.tokens import Doc
from ge.individual import Individual


class Population(object):
    """
    Population implementation of a AI Grammatical Evolution algorithm in OOP fashion
    """

    def __init__(self, samples: [Doc], grammar: dict, size: int):
        """
        Population constructor, initializes a list of Individual objects
        Args:
            samples: list of Spacy doc objets
            grammar: Backus Naur Form grammar notation encoded in a dictionary
            size: Maximum number of individuals per generation
        """
        self._samples = samples
        self._grammar = grammar
        self._size = size
        self._generation = self._initialize()
        self._offspring = list()
        self._max_generations = 200

    def _info(self):
        """
        Prints current generation individuals' fenotype and fitness value
        Returns:

        """
        for individual in self._generation:
            print("Fenotype: ", str(individual._fenotype), "Fitness value: ", individual._fitness_value)

    def _initialize(self) -> [Individual]:
        """
        Initializes the first generation
        Returns: A list of individual objects

        """
        return [Individual(self._samples, self._grammar) for _ in range(0, self._size)]

    ''' Evolutionary specific methods '''
    def _selection(self) -> [Individual]:
        """
        Selects members of the current generation into the mating pool in order to produce offspring
        Returns: a list of individuals

        """
        # TODO(me): k tournament
        ''' Current implementation: Binary Tournament '''
        mating_pool = []

        while len(mating_pool) <= len(self._generation):
            i = random.randint(0, len(self._generation) - 1)
            j = i

            while j == i:
                j = random.randint(0, len(self._generation) - 1)

            i = self._generation[i]
            j = self._generation[j]

            if i._fitness_value >= j._fitness_value:
                mating_pool.append(i)
            else:
                mating_pool.append(j)

        return mating_pool

    def _recombination(self, mating_pool: [Individual]):
        """
        Creates the offspring recombining the mating pool
        Args:
            mating_pool: A list of individuals selected from the current generation

        Returns: A list of new individuals, offspring of the current generation

        """
        offspring = []
        offspring_max_size = round(len(self._generation) * 3.5) # TODO(me): configuration externalization
        mutation_chance = 0.9  # TODO(me): configuration externalization

        while len(offspring) <= offspring_max_size:
            parent_1 = random.choice(mating_pool)
            parent_2 = random.choice(mating_pool)

            if random.random() < mutation_chance:

                cut = random.randint(1, 7) * 10  # One codon far away from start or from end TODO()me: dehardcode

                child_1 = Individual(self._samples, self._grammar,
                                     dna=parent_1._bin_genotype[:cut] + parent_2._bin_genotype[-(80-cut):])
                child_2 = Individual(self._samples, self._grammar,
                                     dna=parent_2._bin_genotype[:cut] + parent_1._bin_genotype[-(80-cut):])

                offspring.append(child_1)
                offspring.append(child_2)

        return offspring

    def _replacement(self) -> None:
        """
        Produces the new generation and cleans up the offspring pool
        Returns: None

        """
        ''' Replacement type:  mu plus lambda
        replacement_pool = self._generation + self._offspring
        replacement_pool.sort(key=lambda i: i._fitness_value, reverse=True)
        self._generation = replacement_pool[:len(self._generation)]
        self._offspring = [] '''

        ''' Replacement type: mu lambda with elitism
        self._generation.sort(key=lambda i: i._fitness_value, reverse=True)
        self._offspring.sort(key=lambda i: i._fitness_value, reverse=True)
        self._generation[1:len(self._generation)] = self._offspring[0:len(self._generation)]
        self._offspring = []'''

        ''' Replacement type: mu lambda without elitism '''
        self._offspring.sort(key=lambda i: i._fitness_value, reverse=True)
        self._generation = self._offspring[0:len(self._generation)]
        self._offspring = []

    def evolve(self):
        """ Search Engine """
        for _ in range(self._max_generations):
            mating_pool = self._selection()
            self._offspring = self._recombination(mating_pool)
            self._replacement()
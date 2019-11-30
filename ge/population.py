""" Population class """
import random
from spacy.tokens import Doc
from spacy.matcher import Matcher
from ge.individual import Individual


class Population(object):
    """ TODO: Docstring """

    def __init__(self, samples: [Doc], grammar: dict, size: int):
        self._samples = samples
        self._grammar = grammar
        self._size = size
        self._generation = self._initialize()
        self._offspring = list()
        self._max_generations = 200

    def _initialize(self) -> [Individual]:
        """ Initializes the first generation  """
        return [Individual(self._samples, self._grammar) for _ in range(0, self._size)]

    def sort(self, individuals: [Individual]):
        """ Sorts individual lists by fitness """
        pass

    def _selection(self):
        """ Selects members of the current generation into the mating pool in order to produce offspring """
        ''' Currently fashion: Binary Tournament '''
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
        """ Creates the offspring recombining the mating pool """
        offspring = []
        offspring_max_size = round(len(self._generation) * 3.5) # TODO configuration externalization
        mutation_chance = 0.9  # TODO configuration externalization

        while len(offspring) <= offspring_max_size:
            parent_1 = random.choice(mating_pool)
            parent_2 = random.choice(mating_pool)

            if random.random() < mutation_chance:

                cut = random.randint(1, 7) * 10  # At least one codon far away from start or from end TODO: dehardcode

                child_1 = Individual(self._samples, self._grammar,
                                     dna=parent_1._bin_genotype[:cut] + parent_2._bin_genotype[-(80-cut):])
                child_2 = Individual(self._samples, self._grammar,
                                     dna=parent_2._bin_genotype[:cut] + parent_1._bin_genotype[-(80-cut):])

                offspring.append(child_1)
                offspring.append(child_2)

        return offspring

    # TODO: Clean if no need
    def _mutate(self, offspring: [Individual]):
        pass

    def _replacement(self):
        """ Produces the new generation """
        ''' Actually mu plus lambda 
        replacement_pool = self._generation + self._offspring
        replacement_pool.sort(key=lambda i: i._fitness_value, reverse=True)
        self._generation = replacement_pool[:len(self._generation)]
        self._offspring = [] '''

        ''' mu lambda with elitism '''
        self._generation.sort(key=lambda i: i._fitness_value, reverse=True)
        self._offspring.sort(key=lambda i: i._fitness_value, reverse=True)
        self._generation[1:len(self._generation)] = self._offspring[0:len(self._generation)]
        self._offspring = []

        ''' mu lambda without elitism
        self._offspring.sort(key=lambda i: i._fitness_value, reverse=True)
        self._generation = self._offspring[0:len(self._generation)]
        self._offspring = [] '''

    def evolve(self):
        """ Search Engine """
        for _ in range(self._max_generations):
            mating_pool = self._selection()
            self._offspring = self._recombination(mating_pool)
            self._replacement()
        # self._info()

    def _info(self):
        for individual in self._generation:
            print("Fenotype: ", str(individual._fenotype), "Fitness: ", individual._fitness_value)

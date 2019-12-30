""" Population class """
import random
from spacy.tokens import Doc
from ge.individual import Individual
from settings.config import Config
from settings.literals import *

config = Config()


class Population(object):
    """ Population implementation of a AI Grammatical Evolution algorithm in OOP fashion """

    def __init__(self, samples: [Doc], grammar: dict):
        """
        Population constructor, initializes a list of Individual objects
        Args:
            samples: list of Spacy doc objets
            grammar: Backus Naur Form grammar notation encoded in a dictionary
        """
        self._samples = samples
        self._grammar = grammar
        self._generation = self._initialize()
        self._offspring = list()
        self._best_individual = None

    def _info(self):
        """
        Prints current generation individuals' fenotype and fitness value
        """
        for individual in self._generation:
            print("Fenotype: ", str(individual._fenotype), "Fitness value: ", individual._fitness_value)

    def _initialize(self) -> [Individual]:
        """
        Initializes the first generation
        Returns: A list of individual objects

        """
        return [Individual(self._samples, self._grammar) for _ in range(0, config._dna_length)]

    def _best_challenge(self):
        """
        Compares current generation best fitness individual against previous generation best fitness individual.
        Updates the best individual attribute accordingly
        """
        if self._best_individual is not None:
            if self._generation[0]._fitness_value > self._best_individual._fitness_value:
                self._best_individual = self._generation[0]
        else:
            self._best_individual = self._generation[0]

    ''' Evolutionary specific methods '''
    def _selection(self) -> [Individual]:
        """
        Selects members of the current generation into the mating pool in order to produce offspring
        Returns: a list of individuals

        """
        if config._selection_type == BINARY_TOURNAMENT:
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
        elif config._selection_type == K_TOURNAMENT:
            # TODO(me): k tournament
            raise NotImplementedError
        else:
            raise ValueError('Invalid selection type: ', config._selection_type)

    def _recombination(self, mating_pool: [Individual]):
        """
        Creates the offspring recombining the mating pool
        Args:
            mating_pool: A list of individuals selected from the current generation

        Returns: A list of new individuals, offspring of the current generation

        """

        if config._recombination_type == RANDOM_ONE_POINT_CROSSOVER:
            offspring = []
            offspring_max_size = round(len(self._generation) * config._offspring_max_size_factor)

            while len(offspring) <= offspring_max_size:
                parent_1 = random.choice(mating_pool)
                parent_2 = random.choice(mating_pool)

                if random.random() < config._mating_probability:
                    cut = random.randint(1, config._codon_length - 1) * config._num_codons_per_individual

                    # Create children
                    child_1 = Individual(self._samples, self._grammar,
                                         dna=parent_1._bin_genotype[:cut] +
                                             parent_2._bin_genotype[-(config._dna_length - cut):])

                    child_2 = Individual(self._samples, self._grammar,
                                         dna=parent_2._bin_genotype[:cut] +
                                             parent_1._bin_genotype[-(config._dna_length - cut):])

                    offspring.append(child_1)
                    offspring.append(child_2)

            return offspring
        else:
            raise ValueError('Invalid recombination type: ', config._recombination_type)

    def _replacement(self) -> None:
        """ Produces the new generation and cleans up the offspring pool  """

        if config._replacement_type == MU_PLUS_LAMBDA:
            replacement_pool = self._generation + self._offspring
            replacement_pool.sort(key=lambda i: i._fitness_value, reverse=True)
            self._generation = replacement_pool[:len(self._generation)]
            self._offspring = []
        elif config._replacement_type == MU_LAMBDA_WITH_ELITISM:
            self._generation.sort(key=lambda i: i._fitness_value, reverse=True)
            self._offspring.sort(key=lambda i: i._fitness_value, reverse=True)
            self._generation[1:len(self._generation)] = self._offspring[0:len(self._generation)]
            self._offspring = []
        elif config._replacement_type == MU_LAMBDA_WITHOUT_ELITISM:
            self._offspring.sort(key=lambda i: i._fitness_value, reverse=True)
            self._generation = self._offspring[0:len(self._generation)]
            self._offspring = []
        else:
            raise ValueError('Invalid replacement type: ', config._replacement_type)

    def evolve(self):
        """ Search Engine """
        for _ in range(config._max_generations):
            mating_pool = self._selection()
            self._offspring = self._recombination(mating_pool)
            self._replacement()
            self._best_challenge()
            # self._info()

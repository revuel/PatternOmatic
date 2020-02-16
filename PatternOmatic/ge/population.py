""" Population class """
import random
from spacy.tokens import Doc
from PatternOmatic.ge.individual import Individual
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.literals import *

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

    ''' Properties & setters '''

    @property
    def samples(self) -> [Doc]:
        return self._samples

    @property
    def grammar(self) -> dict:
        return self._grammar

    @property
    def generation(self) -> [Individual]:
        return self._generation

    @generation.setter
    def generation(self, generation: [Individual]):
        self._generation = generation

    @property
    def offspring(self) -> [Individual]:
        return self._offspring

    @offspring.setter
    def offspring(self, offspring: [Individual]):
        self._offspring = offspring

    @property
    def best_individual(self) -> Individual:
        return self._best_individual

    @best_individual.setter
    def best_individual(self, best_individual: Individual):
        self._best_individual = best_individual

    def _info(self):
        """
        Prints current generation individuals' fenotype and fitness value
        """
        for individual in self.generation:
            print("Fenotype: ", str(individual.fenotype), "Fitness value: ", individual.fitness_value)

    def _initialize(self) -> [Individual]:
        """
        Initializes the first generation
        Returns: A list of individual objects

        """
        return [Individual(self.samples, self.grammar) for _ in range(0, config.dna_length)]

    def _best_challenge(self):
        """
        Compares current generation best fitness individual against previous generation best fitness individual.
        Updates the best individual attribute accordingly
        """
        if self.best_individual is not None:
            if self.generation[0].fitness_value > self.best_individual.fitness_value:
                self.best_individual = self.generation[0]
        else:
            self.best_individual = self.generation[0]

    ''' Evolutionary operators dispatcher '''

    def _selection(self) -> [Individual]:
        """
        Selects members of the current generation into the mating pool in order to produce offspring
        Returns: a list of individuals

        """
        if config.selection_type == BINARY_TOURNAMENT:
            return self._binary_tournament()
        elif config.selection_type == K_TOURNAMENT:
            return self._k_tournament()
        else:
            raise ValueError('Invalid selection type: ', config.selection_type)

    def _recombination(self, mating_pool: [Individual]):
        """
        A pseudo-factory to different recombination types
        Args:
            mating_pool: A list of individuals selected from the current generation

        Returns: A list of new individuals, offspring of the current generation

        """

        if config.recombination_type == RANDOM_ONE_POINT_CROSSOVER:
            return self._random_one_point_crossover(mating_pool)
        else:
            raise ValueError('Invalid recombination type: ', config.recombination_type)

    def _replacement(self) -> None:
        """
        A pseudo-factory to different recombination types

        """

        if config.replacement_type == MU_PLUS_LAMBDA:
            return self._mu_plus_lambda()
        elif config.replacement_type == MU_LAMBDA_WITH_ELITISM:
            return self._mu_lambda_elite()
        elif config.replacement_type == MU_LAMBDA_WITHOUT_ELITISM:
            return self._mu_lambda_no_elite()
        else:
            raise ValueError('Invalid replacement type: ', config.replacement_type)

    ''' Evolutionary operator implementations '''

    def _binary_tournament(self):
        """
        Selection type: Selects members of the current generation into the mating pool in order to produce offspring
        Returns:

        """
        mating_pool = []

        while len(mating_pool) <= len(self.generation):
            i = random.randint(0, len(self.generation) - 1)
            j = i

            while j == i:
                j = random.randint(0, len(self.generation) - 1)

            i = self.generation[i]
            j = self.generation[j]

            if i.fitness_value >= j.fitness_value:
                mating_pool.append(i)
            else:
                mating_pool.append(j)

        return mating_pool

    def _k_tournament(self):
        """
        Selection type: Selects members of the current generation into the mating pool in order to produce offspring
        Returns:

        """
        # TODO(me): k tournament
        raise NotImplementedError

    def _random_one_point_crossover(self, mating_pool: [Individual]) -> [Individual]:
        """
        Recombination type: Creates the offspring recombining the mating pool
        Args:
            mating_pool: A list of individuals selected from the current generation

        Returns: A list of new individuals, offspring of the current generation

        """
        offspring = []
        offspring_max_size = round(len(self.generation) * config.offspring_max_size_factor)

        while len(offspring) <= offspring_max_size:
            parent_1 = random.choice(mating_pool)
            parent_2 = random.choice(mating_pool)

            if random.random() < config.mating_probability:
                cut = random.randint(1, config.codon_length - 1) * config.num_codons_per_individual

                # Create children
                child_1 = Individual(self.samples, self.grammar,
                                     dna=parent_1.bin_genotype[:cut] +
                                         parent_2.bin_genotype[-(config.dna_length - cut):])

                child_2 = Individual(self.samples, self.grammar,
                                     dna=parent_2.bin_genotype[:cut] +
                                         parent_1.bin_genotype[-(config.dna_length - cut):])

                offspring.append(child_1)
                offspring.append(child_2)

        return offspring

    def _mu_plus_lambda(self):
        """
        Replacement type: Produces the new generation and cleans up the offspring pool

        """
        replacement_pool = self.generation + self.offspring
        replacement_pool.sort(key=lambda i: i.fitness_value, reverse=True)
        self.generation = replacement_pool[:len(self.generation)]
        self.offspring = []

    def _mu_lambda_elite(self):
        """
        Replacement type: Produces the new generation and cleans up the offspring pool

        """
        self.generation.sort(key=lambda i: i.fitness_value, reverse=True)
        self.offspring.sort(key=lambda i: i.fitness_value, reverse=True)
        self.generation[1:len(self.generation)] = self.offspring[0:len(self.generation)]
        self.offspring = []

    def _mu_lambda_no_elite(self):
        """
        Replacement type: Produces the new generation and cleans up the offspring pool

        """
        self.offspring.sort(key=lambda i: i.fitness_value, reverse=True)
        self.generation = self.offspring[0:len(self.generation)]
        self.offspring = []

    ''' Evolution '''
    def evolve(self):
        """ Search Engine
        1) Selects individuals of the current generation to constitute who will mate
        2) Crossover or recombination of the previously selected individuals
        3) Replace the this generation with the offspring
        4) Save the best individual by fitness """

        for _ in range(config.max_generations):
            mating_pool = self._selection()
            self.offspring = self._recombination(mating_pool)
            self._replacement()
            self._best_challenge()
            # self._info()

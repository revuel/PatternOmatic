""" Population class """
import random
from typing import List, Tuple

from spacy.tokens import Doc
from PatternOmatic.ge.individual import Individual
from PatternOmatic.ge.stats import Stats
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.literals import SelectionType, RecombinationType, ReplacementType
from PatternOmatic.settings.log import LOG


class Selection(object):
    """ Dispatches the proper selection type for population instances """

    def __init__(self, selection_type):
        self.__dispatch_selection(selection_type)

    def __call__(self, generation, *args, **kwargs) -> List[Individual]:
        LOG.debug(f'Selecting individuals...')
        return self.selection(generation)

    def selection(self, generation) -> List[Individual]:
        """ Gets overridden """
        pass

    def __dispatch_selection(self, selection_type: SelectionType):
        if isinstance(selection_type, SelectionType):
            if selection_type == SelectionType.BINARY_TOURNAMENT:
                self.selection = self._binary_tournament
            elif selection_type == SelectionType.K_TOURNAMENT:
                self.selection = self._k_tournament
        else:
            self.selection = self._binary_tournament

    def _binary_tournament(self, generation):
        """
        Selection type: Selects members of the current generation into the mating pool in order to produce offspring
        Returns:

        """
        mating_pool = []

        while len(mating_pool) <= len(generation):
            i = random.randint(0, len(generation) - 1)
            j = i

            while j == i:
                j = random.randint(0, len(generation) - 1)

            i = generation[i]
            j = generation[j]

            if i.fitness_value >= j.fitness_value:
                mating_pool.append(i)
            else:
                mating_pool.append(j)

        return mating_pool

    def _k_tournament(self, generation):
        """
        Selection type: Selects members of the current generation into the mating pool in order to produce offspring
        Returns:

        """
        # TODO(me): k tournament
        raise NotImplementedError


class Recombination(object):
    """ Dispatches the proper recombination type for population instances """

    def __init__(self, recombination_type, grammar, samples, stats):
        self._config = Config()
        self._grammar = grammar
        self._samples = samples
        self._stats = stats
        self.__dispatch_recombination_type(recombination_type)

    @property
    def config(self):
        return self._config

    @property
    def grammar(self):
        return self._grammar

    @property
    def samples(self):
        return self._samples

    @property
    def stats(self):
        return self._stats

    def __call__(self, mating_pool, generation, *args, **kwargs):
        LOG.debug(f'Combining individuals...')
        return self.recombination(mating_pool, generation)

    def recombination(self, mating_pool: List[Individual], generation: List[Individual]):
        """ Gets overridden """
        pass

    def __dispatch_recombination_type(self, recombination_type: RecombinationType):
        if isinstance(recombination_type, RecombinationType):
            if recombination_type == RecombinationType.RANDOM_ONE_POINT_CROSSOVER:
                self.recombination = self._random_one_point_crossover
            else:
                self.recombination = self._random_one_point_crossover
        else:
            self.recombination = self._random_one_point_crossover

    def _random_one_point_crossover(
            self, mating_pool: List[Individual], generation: List[Individual]) -> List[Individual]:
        """
        Recombination type: Creates the offspring recombining the mating pool
        Args:
            mating_pool: A list of individuals selected from the current generation

        Returns: A list of new individuals, offspring of the current generation

        """
        offspring = []
        offspring_max_size = round(len(generation) * self.config.offspring_max_size_factor)

        while len(offspring) <= offspring_max_size:
            parent_1 = random.choice(mating_pool)
            parent_2 = random.choice(mating_pool)

            if random.random() < self.config.mating_probability:
                cut = random.randint(1, self.config.codon_length - 1) * self.config.num_codons_per_individual

                # Create children
                child_1 = Individual(self.samples, self.grammar, self.stats,
                                     dna=parent_1.bin_genotype[:cut] + parent_2.bin_genotype[
                                                                       -(self.config.dna_length - cut):])

                child_2 = Individual(self.samples, self.grammar, self.stats,
                                     dna=parent_2.bin_genotype[:cut] + parent_1.bin_genotype[
                                                                 -(self.config.dna_length - cut):])

                offspring.append(child_1)
                offspring.append(child_2)

        return offspring


class Replacement(object):
    """ Dispatches the proper recombination type for population instances """
    def __init__(self, replacement_type):
        self.__dispatch_replacement_type(replacement_type)

    def __call__(self, generation, offspring, *args, **kwargs) -> Tuple[List[Individual], List[Individual]]:
        return self.replacement(generation, offspring)

    def replacement(self):
        pass

    def __dispatch_replacement_type(self, replacement_type: ReplacementType):
        if isinstance(replacement_type, ReplacementType):
            if replacement_type == ReplacementType.MU_PLUS_LAMBDA:
                self.replacement = self._mu_plus_lambda
            elif replacement_type == ReplacementType.MU_LAMBDA_WITH_ELITISM:
                self.replacement = self._mu_lambda_elite
            elif replacement_type == ReplacementType.MU_LAMBDA_WITHOUT_ELITISM:
                self.replacement = self._mu_lambda_no_elite
        else:
            self.replacement = self._mu_plus_lambda

    def _mu_plus_lambda(self, generation, offspring):
        """
        Replacement type: Produces the new generation and cleans up the offspring pool

        """
        replacement_pool = generation + offspring
        replacement_pool.sort(key=lambda i: i.fitness_value, reverse=True)
        generation = replacement_pool[:len(generation)]
        offspring = []

        return generation, offspring

    def _mu_lambda_elite(self, generation, offspring):
        """
        Replacement type: Produces the new generation and cleans up the offspring pool

        """
        generation.sort(key=lambda i: i.fitness_value, reverse=True)
        offspring.sort(key=lambda i: i.fitness_value, reverse=True)
        generation[1:len(generation)] = offspring[0:len(generation)]
        offspring = []

        return generation, offspring

    def _mu_lambda_no_elite(self, generation, offspring):
        """
        Replacement type: Produces the new generation and cleans up the offspring pool

        """
        offspring.sort(key=lambda i: i.fitness_value, reverse=True)
        generation = offspring[0:len(generation)]
        offspring = []

        return generation, offspring


class Population(object):
    """ Population implementation of an AI Grammatical Evolution algorithm in OOP fashion """

    def __init__(self, samples: [Doc], grammar: dict, stats: Stats):
        """
        Population constructor, initializes a list of Individual objects
        Args:
            samples: list of Spacy doc objets
            grammar: Backus Naur Form grammar notation encoded in a dictionary
        """
        self._config = Config()

        self._samples = samples
        self._grammar = grammar
        self._stats = stats
        self._generation = self._genesis()
        self._offspring = list()
        self._best_individual = None

        self.selection = Selection(self._config.selection_type)
        self.recombination = Recombination(self._config.recombination_type, grammar, samples, stats)
        self.replacement = Replacement(self._config.replacement_type)

    #
    # Properties & setters
    #
    @property
    def config(self) -> Config:
        return self._config

    @property
    def samples(self) -> [Doc]:
        return self._samples

    @property
    def grammar(self) -> dict:
        return self._grammar

    @property
    def stats(self):
        return self._stats

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

    def _genesis(self) -> [Individual]:
        """
        Initializes the first generation
        Returns: A list of individual objects

        """
        return [Individual(self.samples, self.grammar, self.stats) for _ in range(0, self.config.dna_length)]

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

    #
    # Evolution
    #
    def evolve(self):
        """ Search Engine
        1) Selects individuals of the current generation to constitute who will mate
        2) Crossover or recombination of the previously selected individuals
        3) Replace/mix the this generation with the offspring
        4) Save the best individual by fitness
        5) Calculates statistics for this Run """

        LOG.info('Evolution taking place!')

        self.stats.reset()

        for _ in range(self.config.max_generations):
            mating_pool = self.selection(self.generation)
            self.offspring = self.recombination(mating_pool, self.generation)
            self.generation, self.offspring = self.replacement(self.generation, self.offspring)
            self._best_challenge()

        LOG.info(f'Best candidate found on this run: {dict(self.best_individual)}')

        # Stats concerns
        self.stats.add_most_fitted(self.best_individual)
        self.stats.add_mbf(self.best_individual.fitness_value)

        if self.best_individual.fitness_value > self.config.success_threshold:
            self.stats.add_sr(True)
        else:
            self.stats.add_sr(False)

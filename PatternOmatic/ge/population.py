""" Evolutionary Population related classes module

This file is part of PatternOmatic.

Copyright © 2020  Miguel Revuelta Espinosa

PatternOmatic is free software: you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License
as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

PatternOmatic is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with PatternOmatic. If not, see <https://www.gnu.org/licenses/>.

"""
import random
from typing import List, Tuple, Dict
from spacy.tokens import Doc

from PatternOmatic.ge.individual import Individual
from PatternOmatic.ge.stats import Stats
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.literals import SelectionType, ReplacementType
from PatternOmatic.settings.log import LOG


class Selection(object):
    """ Dispatches the proper selection type for population instances """
    __slots__ = '_select'

    def __init__(self, selection_type: SelectionType):
        self.__dispatch_selection(selection_type)

    def __call__(self, generation: List[Individual]) -> List[Individual]:
        """
        Performs a selection operation for the population
        Args:
            generation: A list of Individual instances

        Returns: A list of Individual instances

        """
        LOG.debug(f'Selecting individuals...')
        return self._select(generation)

    def __dispatch_selection(self, selection_type: SelectionType) -> None:
        """
        Sets the type of the selection operation for the current evolution
        Args:
            selection_type: SelectionType Enum

        Returns: None

        """
        if isinstance(selection_type, SelectionType):
            if selection_type == SelectionType.K_TOURNAMENT:
                self._select = self._k_tournament
            else:
                self._select = self._binary_tournament
        else:
            self._select = self._binary_tournament

    @staticmethod
    def _binary_tournament(generation: List[Individual]) -> List[Individual]:
        """
        Selects members of the current generation into the mating pool in order to produce offspring by comparing pairs
        of Individuals and adding the best of each pair to the "mating pool" until its filled

        Args:
            generation: A list of Individual instances

        Returns: A list of Individual instances

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

    @staticmethod
    def _k_tournament(generation: List[Individual]) -> List[Individual]:
        """
        Not implemented
        Args:
            generation: A list of Individual instances

        Raises: NotImplementedError
        Returns: A list of Individual instances

        """
        # TODO(me): k tournament
        raise NotImplementedError


class Recombination(object):
    """ Dispatches the proper recombination type for population instances """
    __slots__ = ('_recombine', 'config', 'grammar', 'samples', 'stats')

    def __init__(self, grammar: Dict, samples: List[Doc], stats: Stats):
        self._recombine = None
        self.config = Config()
        self.grammar = grammar
        self.samples = samples
        self.stats = stats
        self.__dispatch_recombination_type()

    def __call__(self, mating_pool: List[Individual], generation: List[Individual]) -> List[Individual]:
        LOG.debug(f'Combining individuals...')
        return self._recombine(mating_pool, generation)

    def __dispatch_recombination_type(self) -> None:
        """
        Sets the type of the selection operation for the current evolution

        Returns: None

        """
        self._recombine = self._random_one_point_crossover

    def _random_one_point_crossover(
            self, mating_pool: List[Individual], generation: List[Individual]) -> List[Individual]:
        """
        For each pair of Individual instances, recombines them produce two offsprings. Puts them all into the offspring
        Args:
            mating_pool: A list of Individual instances
            generation: A list of Individual instances

        Returns: A list of Individual instances

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
    __slots__ = '_replace'

    def __init__(self, replacement_type: ReplacementType):
        self.__dispatch_replacement_type(replacement_type)

    def __call__(self, generation: List[Individual], offspring: List[Individual]) \
            -> Tuple[List[Individual], List[Individual]]:
        LOG.debug(f'Replacing individuals...')
        return self._replace(generation, offspring)

    def __dispatch_replacement_type(self, replacement_type: ReplacementType) -> None:
        """
        Sets the type of the replacement operation for the current evolution
        Args:
            replacement_type: ReplacementType Enum

        Returns: None

        """
        if isinstance(replacement_type, ReplacementType):
            if replacement_type == ReplacementType.MU_LAMBDA_WITH_ELITISM:
                self._replace = self._mu_lambda_elite
            elif replacement_type == ReplacementType.MU_LAMBDA_WITHOUT_ELITISM:
                self._replace = self._mu_lambda_no_elite
            else:
                self._replace = self._mu_plus_lambda
        else:
            self._replace = self._mu_plus_lambda

    @staticmethod
    def _mu_plus_lambda(generation: List[Individual], offspring: List[Individual]) \
            -> Tuple[List[Individual], List[Individual]]:
        """
        Produces the next generation combining the current generation with the offspring
        Args:
            generation: A list of Individual instances
            offspring: A list of Individual instances

        Returns: A tuple containing two list of Individual instances

        """
        replacement_pool = generation + offspring
        replacement_pool.sort(key=lambda i: i.fitness_value, reverse=True)
        generation = replacement_pool[:len(generation)]
        offspring = []

        return generation, offspring

    @staticmethod
    def _mu_lambda_elite(generation: List[Individual], offspring: List[Individual]) \
            -> Tuple[List[Individual], List[Individual]]:
        """
        Produces the next generation using the offspring and the best Individual of the current generation
        Args:
            generation: A list of Individual instances
            offspring: A list of Individual instances

        Returns: A tuple containing two list of Individual instances

        """
        generation.sort(key=lambda i: i.fitness_value, reverse=True)
        offspring.sort(key=lambda i: i.fitness_value, reverse=True)
        generation[1:len(generation)] = offspring[0:len(generation)]
        offspring = []

        return generation, offspring

    @staticmethod
    def _mu_lambda_no_elite(generation: List[Individual], offspring: List[Individual]) \
            -> Tuple[List[Individual], List[Individual]]:
        """
        Produces the next generation totally replacing the current generation with the offspring
        Args:
            generation: A list of Individual instances
            offspring: A list of Individual instances

        Returns: A tuple containing two list of Individual instances

        """
        offspring.sort(key=lambda i: i.fitness_value, reverse=True)
        generation = offspring[0:len(generation)]
        offspring = []

        return generation, offspring


class Population(object):
    """ Population implementation of an AI Grammatical Evolution algorithm in OOP fashion """
    __slots__ = ('config', 'samples', 'grammar', 'stats', 'generation', 'offspring', 'best_individual',
                 'selection', 'recombination', 'replacement')

    def __init__(self, samples: [Doc], grammar: dict, stats: Stats):
        """
        Population constructor, initializes a list of Individual objects
        Args:
            samples: list of Spacy doc objets
            grammar: Backus Naur Form grammar notation encoded in a dictionary
        """
        self.config = Config()

        self.samples = samples
        self.grammar = grammar
        self.stats = stats
        self.generation = self._genesis()
        self.offspring = list()
        self.best_individual = None

        self.selection = Selection(self.config.selection_type)
        self.recombination = Recombination(grammar, samples, stats)
        self.replacement = Replacement(self.config.replacement_type)

    #
    # Population specific methods
    #
    def _genesis(self) -> List[Individual]:
        """
        Initializes the first generation
        Returns: A list of individual objects

        """
        return [Individual(self.samples, self.grammar, self.stats) for _ in range(0, self.config.dna_length)]

    def _best_challenge(self) -> None:
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
        """
        Search Engine:
            1) Selects individuals of the current generation to constitute who will mate
            2) Crossover or recombination of the previously selected individuals
            3) Replace/mix the this generation with the offspring
            4) Save the best individual by fitness
            5) Calculate statistics for this Run
        """

        LOG.info('Evolution taking place, please wait...')

        self.stats.reset()

        for _ in range(self.config.max_generations):
            mating_pool = self.selection(self.generation)
            self.offspring = self.recombination(mating_pool, self.generation)
            self.generation, self.offspring = self.replacement(self.generation, self.offspring)
            self._best_challenge()

        LOG.info(f'Best candidate found on this run: {self.best_individual}')

        # Stats concerns
        self.stats.add_most_fitted(self.best_individual)
        self.stats.add_mbf(self.best_individual.fitness_value)

        if self.best_individual.fitness_value > self.config.success_threshold:
            self.stats.add_sr(True)
        else:
            self.stats.add_sr(False)

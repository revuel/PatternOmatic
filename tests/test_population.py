""" Unit testing module for GE Population module

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
import unittest
import spacy

from PatternOmatic.ge.stats import Stats
from PatternOmatic.nlp.bnf import dynamic_generator as dgg
from PatternOmatic.ge.population import Population, Selection, Recombination, Replacement
from PatternOmatic.ge.individual import Individual
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.literals import FitnessType, SelectionType, RecombinationType, ReplacementType


class BasePopulationTest(unittest.TestCase):
    """ Base class to supply shard attributes and helpers """
    #
    # Shared attributes
    #
    config = Config()

    nlp = spacy.load("en_core_web_sm")

    samples = [nlp(u'I am a raccoon!'),
               nlp(u'You are a cat!'),
               nlp(u'Is she a rabbit?'),
               nlp(u'This is a test')]

    grammar = dgg(samples)

    stats = Stats()

    #
    # Helpers
    #
    def setUp(self) -> None:
        """ Fresh Config instance """
        self.config = Config()

    def tearDown(self) -> None:
        """ Destroy Config instance """
        Config.clear_instance()


class TestPopulation(BasePopulationTest):
    """ Unit Test class for GE Population object """

    def test_initialize(self):
        """ Tests that a population is correctly filled with Individuals """
        p = Population(self.samples, self.grammar, self.stats)

        super().assertIsInstance(p.generation[0], Individual)

    def test_best_challenge(self):
        """ Tests that the most fitted individual occupies the population's best_individual slot """
        self.config.max_generations = 3
        self.config.fitness_function_type = FitnessType.BASIC
        p = Population(self.samples, self.grammar, self.stats)
        self.config.mutation_probability = 0.0
        p.generation[0] = Individual(self.samples, self.grammar, self.stats, '01110101100101100110010110010101')
        self.config.mutation_probability = 0.5
        p.evolve()

        super().assertGreaterEqual(p.best_individual.fitness_value, 0.2)

    def test_binary_tournament(self):
        """ Test that binary tournament works as expected """
        self.config.max_generations = 3
        self.config.fitness_function_type = FitnessType.FULL_MATCH
        self.config.selection_type = SelectionType.BINARY_TOURNAMENT
        p = Population(self.samples, self.grammar, self.stats)
        mating_pool = p.selection(p.generation)

        super().assertNotEqual(p.generation, mating_pool)

    def test_k_tournament(self):
        """ Test that k tournament raises error """
        self.config.selection_type = SelectionType.K_TOURNAMENT
        p = Population(self.samples, self.grammar, self.stats)
        with super().assertRaises(NotImplementedError):
            _ = p.selection(p.generation)

    def test_random_one_point_crossover(self):
        """ Test that crossover 'random one point' works as expected """
        self.config.max_generations = 3
        self.config.fitness_function_type = FitnessType.BASIC
        self.config.selection_type = SelectionType.BINARY_TOURNAMENT
        self.config.recombination_type = RecombinationType.RANDOM_ONE_POINT_CROSSOVER
        p = Population(self.samples, self.grammar, self.stats)
        mating_pool = p.selection(p.generation)
        p.offspring = p.recombination(mating_pool, p.generation)
        super().assertNotEqual(p.generation, p.offspring)

    def test_mu_plus_lambda(self):
        """ Tests that replacement 'mu plus lambda' works as expected """
        self.config.replacement_type = ReplacementType.MU_PLUS_LAMBDA
        p = Population(self.samples, self.grammar, self.stats)
        mating_pool = p.selection(p.generation)
        p.offspring = p.recombination(mating_pool, p.generation)
        p.generation, p.offspring = p.replacement(p.generation, p.offspring)
        super().assertListEqual(p.offspring, [])

    def test_mu_lambda_elite(self):
        """ Tests that replacement 'mu lambda with elitism' works as expected """
        self.config.replacement_type = ReplacementType.MU_LAMBDA_WITH_ELITISM
        p = Population(self.samples, self.grammar, self.stats)
        mating_pool = p.selection(p.generation)
        p.offspring = p.recombination(mating_pool, p.generation)
        p.generation, p.offspring = p.replacement(p.generation, p.offspring)
        super().assertListEqual(p.offspring, [])

    def test_mu_lambda_no_elite(self):
        """ Tests that replacement 'mu lambda without elitism' works as expected """
        self.config.replacement_type = ReplacementType.MU_LAMBDA_WITHOUT_ELITISM
        p = Population(self.samples, self.grammar, self.stats)
        mating_pool = p.selection(p.generation)
        p.offspring = p.recombination(mating_pool, p.generation)
        p.generation, p.offspring = p.replacement(p.generation, p.offspring)
        super().assertListEqual(p.offspring, [])

    def test_evolve(self):
        """ Tests that an evolution works, preserving a fitted individual """
        self.config.max_generations = 3
        self.config.fitness_function_type = FitnessType.BASIC
        p = Population(self.samples, self.grammar, self.stats)
        self.config.mutation_probability = 0.0
        p.generation[0] = Individual(self.samples, self.grammar, self.stats, '01110101100101100110010110010101')
        self.config.mutation_probability = 0.5
        p.evolve()
        super().assertLessEqual(0.25, p.generation[0].fitness_value)

    def test_best_challenge_changes_best_individual(self):
        """ Covers best challenge cases """
        self.config.mutation_probability = 0.0
        self.config.fitness_function_type = FitnessType.BASIC

        p = Population(self.samples, self.grammar, self.stats)
        i1 = Individual(self.samples, self.grammar, self.stats, dna='00000000000000000000000000000000')
        i2 = Individual(self.samples, self.grammar, self.stats, dna='01110101100101100110010110010101')

        # When there's no best individual yet, population's best individual is updated
        p.best_individual = None
        p.generation = [i2]
        p._best_challenge()

        super().assertEqual(p.best_individual, p.generation[0])

        # When a better individual is better fitted in a new generation, population's best individual is updated
        p.best_individual = i1
        p.generation = [i2]
        p._best_challenge()

        super().assertEqual(p.best_individual, p.generation[0])

        # When a worse individual is the most fitted in a new generation, population's best individual remains the same
        p.best_individual = i2
        p.generation = [i1]
        p._best_challenge()

        super().assertEqual(i2, p.best_individual)

    def test_sr_update(self):
        """ Check SR is updated if a solution is found for the run """
        stats = Stats()

        self.config.max_generations = 1
        self.config.population_size = 3
        self.config.fitness_function_type = FitnessType.BASIC
        self.config.mutation_probability = 0.0

        self.config.success_threshold = 0.0
        p = Population(self.samples, self.grammar, stats)
        p.generation[0] = Individual(self.samples, self.grammar, stats, '01110101100101100110010110010101')
        p.evolve()
        super().assertListEqual([True], stats.success_rate_accumulator)

        self.config.success_threshold = 1.0
        self.config.population_size = 1
        p = Population(self.samples, self.grammar, stats)
        p.generation[0] = Individual(self.samples, self.grammar, stats, '00000000000000000000000000000000')
        p.evolve()
        super().assertListEqual([True, False], stats.success_rate_accumulator)


class TestSelection(BasePopulationTest):
    """ Unit Test class for GE Selection object """

    def test_dispatch(self):
        """ Dispatcher method provides the proper selection method """
        selection = Selection(SelectionType.BINARY_TOURNAMENT)
        super().assertIs(selection._select, Selection._binary_tournament)

        selection = Selection(SelectionType.K_TOURNAMENT)
        super().assertIs(selection._select, Selection._k_tournament)

        # Check unknown SelectionType
        selection = Selection(None)
        super().assertIs(selection._select, Selection._binary_tournament)


class TestRecombination(BasePopulationTest):
    """ Unit Test class for GE Recombination object """

    def test_dispatch(self):
        """ Dispatcher method provides the proper recombine method """
        recombination = Recombination(self.grammar, self.samples, self.stats)
        super().assertEqual(recombination._recombine, recombination._random_one_point_crossover)


class TestReplacement(BasePopulationTest):
    """ Unit Test class for GE Replacement object """

    def test_dispatch(self):
        """ Dispatcher method provides the proper replacement method """
        replacement = Replacement(ReplacementType.MU_PLUS_LAMBDA)
        super().assertIs(replacement._replace, Replacement._mu_plus_lambda)

        replacement = Replacement(ReplacementType.MU_LAMBDA_WITH_ELITISM)
        super().assertIs(replacement._replace, Replacement._mu_lambda_elite)

        replacement = Replacement(ReplacementType.MU_LAMBDA_WITHOUT_ELITISM)
        super().assertIs(replacement._replace, Replacement._mu_lambda_no_elite)

        # Check unknown ReplacementType
        replacement = Replacement(None)
        super().assertIs(replacement._replace, Replacement._mu_plus_lambda)


if __name__ == "__main__":
    unittest.main()

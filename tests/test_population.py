""" Unit testing file for GE module """
import unittest
import spacy

from PatternOmatic.ge.stats import Stats
from PatternOmatic.nlp.engine import dynagg as dgg
from PatternOmatic.ge.population import Population
from PatternOmatic.ge.individual import Individual
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.literals import *


class TestPopulation(unittest.TestCase):
    """ Unit Test class for GE Population object """
    config = Config()

    nlp = spacy.load("en_core_web_sm")

    samples = [nlp(u'I am a raccoon!'),
               nlp(u'You are a cat!'),
               nlp(u'Is she a rabbit?'),
               nlp(u'This is a test')]

    grammar = dgg(samples)

    stats = Stats()

    def test_initialize(self):
        """ Tests that a population is correctly filled with Individuals """
        p = Population(self.samples, self.grammar, self.stats)
        super().assertIsInstance(p.generation[0], Individual)

    def test_best_challenge(self):
        """ Tests that the most fitted individual occupies the population's best_individual slot """
        self.config.max_generations = 3
        self.config.fitness_function_type = FITNESS_BASIC
        p = Population(self.samples, self.grammar, self.stats)
        self.config.mutation_probability = 0.0
        p.generation[0] = Individual(self.samples, self.grammar, self.stats, '01110101100101100110010110010101')
        self.config.mutation_probability = 0.5
        p.evolve()

        super().assertGreaterEqual(p.best_individual.fitness_value, 0.2)

    def test_binary_tournament(self):
        """ Test that binary tournament works as expected """
        self.config.max_generations = 3
        self.config.fitness_function_type = FITNESS_FULLMATCH
        self.config.selection_type = BINARY_TOURNAMENT
        p = Population(self.samples, self.grammar, self.stats)
        mating_pool = p._selection()

        super().assertNotEqual(p.generation, mating_pool)

    def test_k_tournament(self):
        """ Test that k tournament raises error """
        self.config.selection_type = K_TOURNAMENT
        p = Population(self.samples, self.grammar, self.stats)
        with super().assertRaises(NotImplementedError):
            _ = p._selection()
        self.config.selection_type = BINARY_TOURNAMENT

    def test_random_one_point_crossover(self):
        """ Test that crossover 'random one point' works as expected """
        self.config.max_generations = 3
        self.config.fitness_function_type = FITNESS_BASIC
        self.config.selection_type = BINARY_TOURNAMENT
        self.config.recombination_type = RANDOM_ONE_POINT_CROSSOVER
        p = Population(self.samples, self.grammar, self.stats)
        mating_pool = p._selection()
        p.offspring = p._recombination(mating_pool)
        super().assertNotEqual(p.generation, p.offspring)

    def test_mu_plus_lambda(self):
        """ Tests that replacement 'mu plus lambda' works as expected """
        self.config.replacement_type = MU_PLUS_LAMBDA
        p = Population(self.samples, self.grammar, self.stats)
        mating_pool = p._selection()
        p.offspring = p._recombination(mating_pool)
        p._replacement()
        super().assertListEqual(p.offspring, [])

    def test_mu_lambda_elite(self):
        """ Tests that replacement 'mu lambda with elitism' works as expected """
        self.config.replacement_type = MU_LAMBDA_WITH_ELITISM
        p = Population(self.samples, self.grammar, self.stats)
        mating_pool = p._selection()
        p.offspring = p._recombination(mating_pool)
        p._replacement()
        super().assertListEqual(p.offspring, [])

    def test_mu_lambda_no_elite(self):
        """ Tests that replacement 'mu lambda without elitism' works as expected """
        self.config.replacement_type = MU_LAMBDA_WITHOUT_ELITISM
        p = Population(self.samples, self.grammar, self.stats)
        mating_pool = p._selection()
        p.offspring = p._recombination(mating_pool)
        p._replacement()
        super().assertListEqual(p.offspring, [])

    def test_evolve(self):
        """ Tests that an evolution works, preserving a fitted individual """
        self.config.max_generations = 3
        self.config.fitness_function_type = FITNESS_BASIC
        p = Population(self.samples, self.grammar, self.stats)
        self.config.mutation_probability = 0.0
        p.generation[0] = Individual(self.samples, self.grammar, self.stats, '01110101100101100110010110010101')
        self.config.mutation_probability = 0.5
        p.evolve()
        super().assertGreaterEqual(p.generation[0].fitness_value, 0.2)

    def setUp(self) -> None:
        self.config = Config()

    def tearDown(self) -> None:
        Config.clear_instance()


if __name__ == "__main__":
    unittest.main()

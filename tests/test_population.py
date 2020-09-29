""" Unit testing file for GE module """
import unittest
import spacy

from PatternOmatic.ge.stats import Stats
from PatternOmatic.nlp.bnf import dynamic_generator as dgg
from PatternOmatic.ge.population import Population
from PatternOmatic.ge.individual import Individual
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.literals import FitnessType, SelectionType, RecombinationType, ReplacementType


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
        super().assertGreaterEqual(p.generation[0].fitness_value, 0.2)

    def test_best_challenge_changes_best_individual(self):
        """ Covers best challenge cases """
        p = Population(self.samples, self.grammar, self.stats)
        i1 = Individual(self.samples, self.grammar, self.stats, dna='00000000000000000000000000000000')
        i2 = Individual(self.samples, self.grammar, self.stats, dna='01110101100101100110010110010101')

        # When there's no best individual yet, population's best individual is updated
        p.best_individual = None
        p.generation = [i2]
        p._best_challenge()

        super().assertEqual(i2, p.generation[0])

        # When a better individual is the most fitted in a new generation, population's best individual is updated
        p.best_individual = i1
        p.generation = [i2]
        p._best_challenge()

        super().assertEqual(i2, p.generation[0])

        # When a worse individual is the most fitted in a new generation, population's best individual remains the same
        p.best_individual = i2
        p.generation = [i1]
        p._best_challenge()

        super().assertEqual(i2, p.best_individual)

    #
    # Helpers
    #
    def setUp(self) -> None:
        """ Fresh Config instance """
        self.config = Config()

    def tearDown(self) -> None:
        """ Destroy Config instance, reset Underscore's token extensions """
        Config.clear_instance()


if __name__ == "__main__":
    unittest.main()

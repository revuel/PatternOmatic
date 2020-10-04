""" Unit testing file for GE module """
import unittest
import spacy

from PatternOmatic.ge.stats import Stats
from PatternOmatic.nlp.bnf import dynamic_generator as dgg
from PatternOmatic.ge.individual import Individual, Fitness
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.literals import FitnessType


class TestIndividual(unittest.TestCase):
    """ Unit Test class for GE Individual object """
    config = Config()

    nlp = spacy.load("en_core_web_sm")

    samples = [nlp(u'I am a raccoon!'),
               nlp(u'You are a cat!'),
               nlp(u'Is she a rabbit?'),
               nlp(u'This is a test')]

    grammar = dgg(samples)

    stats = Stats()

    def test_init(self):
        """ Test that Individual instantiation works"""
        i = Individual(self.samples, self.grammar, self.stats)
        super().assertNotEqual(i, None)

    def test_init_with_dna(self):
        """ Test that Individual instantiation works when providing dna"""
        i = Individual(self.samples, self.grammar, self.stats,  '10101010101010101010101010101010')
        super().assertNotEqual(i, None)

    def test_transcription(self):
        """ Check for transcription idempotency """
        self.config.mutation_probability = 0.0
        i = Individual(self.samples, self.grammar, self.stats, '11111111')
        i._transcription()
        i._transcription()
        i._transcription()

        super().assertListEqual(i.int_genotype, [127, 1])

    def test_translation(self):
        """ Check for translation idempotency """
        self.config.mutation_probability = 0.0
        i = Individual(self.samples, self.grammar, self.stats, '11111111')
        i._translation()
        i._translation()
        i._translation()
        super().assertListEqual(
            i.fenotype, [{'TEXT': 'am'}, {'TEXT': '?'}, {'TEXT': 'am'}, {'TEXT': '?'}, {'TEXT': 'am'}])

    def test_mutation(self):
        """ Checks that mutation works """
        self.config.mutation_probability = 1.0
        i = Individual(self.samples, self.grammar, self.stats, '11111111')
        super().assertNotEqual(i.bin_genotype, '11111111')

    def test_fitness_basic(self):
        """ Fitness "basic" sets fitness """
        self.config.mutation_probability = 0.0
        self.config.fitness_function_type = FitnessType.BASIC
        i = Individual(self.samples, self.grammar, self.stats, '01110101100101100110010110010101')

        super().assertEqual(i.fitness_value, 0.25)

    def test_fitness_full_match(self):
        """ Fitness "full match" sets fitness """
        self.config.mutation_probability = 0.0
        self.config.fitness_function_type = FitnessType.FULL_MATCH
        i = Individual(self.samples, self.grammar, self.stats, '01101010100001101000110111000100')

        super().assertEqual(i.fitness_value, 0.25)

    def test_token_wildcard_penalty(self):
        """ Checks that token wildcard penalty is properly set """
        # When using token wildcard, penalty is applied
        f = object.__new__(Fitness)
        f.fenotype = [{}, {}, {}, 'Whatever']
        self.config.use_token_wildcard = True
        f.config = self.config
        super().assertEqual(0.25, f._wildcard_penalty(1.0))

        # When not using token wildcard, penalty is not applied
        self.config.use_token_wildcard = False
        f.fenotype = 1.0
        super().assertEqual(1.0, f._wildcard_penalty(1.0))

    #
    # Helpers
    #
    def setUp(self) -> None:
        """ Fresh Config instance """
        self.config = Config()

    def tearDown(self) -> None:
        """ Destroy Config instance """
        Config.clear_instance()


if __name__ == "__main__":
    unittest.main()

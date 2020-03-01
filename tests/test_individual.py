""" Unit testing file for GE module """
import unittest
import spacy

from PatternOmatic.ge.stats import Stats
from PatternOmatic.nlp.engine import dynagg as dgg
from PatternOmatic.ge.individual import Individual
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.literals import *

config = Config()


class TestIndividual(unittest.TestCase):
    """ Unit Test class for GE Individual object """
    nlp = spacy.load("en_core_web_sm")

    samples = [nlp(u'I am a raccoon!'),
               nlp(u'You are a cat!'),
               nlp(u'Is she a rabbit?'),
               nlp(u'This is a test')]

    grammar = dgg(samples)

    stats = Stats()

    def test_init(self):
        i = Individual(self.samples, self.grammar, self.stats)
        super().assertNotEqual(i, None)

    def test_init_with_dna(self):
        i = Individual(self.samples, self.grammar, self.stats,  '10101010101010101010101010101010')
        super().assertNotEqual(i, None)

    def test_transcription(self):
        """ Check for transcription idempotency """
        config.mutation_probability = 0.0
        i = Individual(self.samples, self.grammar, self.stats, '11111111')
        i._transcription()
        i._transcription()
        i._transcription()

        super().assertListEqual(i.int_genotype, [127, 1])

    def test_translation(self):
        """ Check for translation idempotency """
        config.mutation_probability = 0.0
        i = Individual(self.samples, self.grammar, self.stats, '11111111')
        i._translation()
        i._translation()
        i._translation()
        super().assertListEqual(
            i.fenotype, [{'TEXT': '?'}, {'TEXT': 'am'}, {'TEXT': '?'}, {'TEXT': 'am'}, {'TEXT': '?'}])

    def test_mutation(self):
        config.mutation_probability = 1.0
        i = Individual(self.samples, self.grammar, self.stats, '11111111')
        super().assertNotEqual(i.bin_genotype, '11111111')

    def test_fitness_basic(self):
        """ Fitness "basic" sets fitness """
        config.mutation_probability = 0.0
        config.fitness_function_type = FITNESS_BASIC
        i = Individual(self.samples, self.grammar, self.stats, '00101001011010000011001111001110')

        super().assertEqual(i.fitness_value, 0.4)

    def test_fitness_fullmatch(self):
        """ Fitness "full match" sets fitness """
        config.mutation_probability = 0.0
        config.fitness_function_type = FITNESS_FULLMATCH
        i = Individual(self.samples, self.grammar, self.stats, '11100010101000111001010100111011')

        super().assertEqual(i.fitness_value, 0.25)


if __name__ == "__main__":
    unittest.main()

""" Unit testing file for GE module """
import unittest
import spacy
from src.nlp.engine import dynagg as dgg
from src.ge.individual import Individual
from src.settings.config import Config
from src.settings.literals import *

config = Config()


class TestIndividual(unittest.TestCase):
    """ Unit Test class for GE Individual object """
    nlp = spacy.load("en_core_web_sm")

    samples = [nlp(u'I am a raccoon!'),
               nlp(u'You are a cat!'),
               nlp(u'Is she a rabbit?'),
               nlp(u'This is a test')]

    grammar = dgg(samples)

    def test_init(self):
        i = Individual(self.samples, self.grammar)
        assert i is not None

    def test_init_with_dna(self):
        i = Individual(self.samples, self.grammar, '10101010101010101010101010101010')
        assert i is not None

    def test_transcription(self):
        """ Check for transcription idempotency """
        config.mutation_probability = 0.0
        i = Individual(self.samples, self.grammar, '11111111')
        i._transcription()
        i._transcription()
        i._transcription()
        assert i.int_genotype == [127, 1]

    def test_translation(self):
        """ Check for translation idempotency """
        config.mutation_probability = 0.0
        i = Individual(self.samples, self.grammar, '11111111')
        i._translation()
        i._translation()
        i._translation()
        assert i.fenotype == [{'TEXT': '?'}, {'TEXT': 'am'}, {'TEXT': '?'}, {'TEXT': 'am'}, {'TEXT': '?'}]

    def test_mutation(self):
        i = Individual(self.samples, self.grammar, '11111111')
        assert i.bin_genotype is not '11111111'

    def test_fitness_basic(self):
        """ Fitness "basic" sets fitness """
        config.mutation_probability = 0.0
        config.fitness_function_type = FITNESS_BASIC
        i = Individual(self.samples, self.grammar, '00101001011010000011001111001110')
        assert i.fitness_value == 0.4

    def test_fitness_fullmatch(self):
        """ Fitness "full match" sets fitness """
        config.mutation_probability = 0.0
        config.fitness_function_type = FITNESS_FULLMATCH
        i = Individual(self.samples, self.grammar, '11100010101000111001010100111011')
        assert i.fitness_value == 0.25


if __name__ == "__main__":
    unittest.main()

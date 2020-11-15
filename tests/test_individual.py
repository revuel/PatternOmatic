""" Unit testing module for GE Individual module

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
from PatternOmatic.ge.individual import Individual, Fitness
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.literals import FitnessType, S, P, T, F, ORTH, TOKEN_WILDCARD, UNDERSCORE, IS_CURRENCY, \
    NOT_IN, ZERO_OR_MORE, OP, GTH, XPS, IN


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
        """ Test that Individual instantiation works """
        i = Individual(self.samples, self.grammar, self.stats)
        super().assertIs(type(i), Individual)

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

    def test_translate(self):
        """ Verifies conversions over the BNF are done correctly """
        i = object.__new__(Individual)

        # Root
        i.grammar = {S: [P]}
        super().assertEqual('"S":"<P>"', i._translate(0, S, S))

        # Pattern root symbol to Token symbol
        i.grammar = {P: [T]}
        super().assertEqual(T, i._translate(0, P, P))

        # Token symbol to Feature symbol inside Token
        i.grammar = {T: [F]}
        super().assertEqual('{<F>}', i._translate(0, T, T))

        # Token symbol to wildcard
        i.grammar = {T: [TOKEN_WILDCARD]}
        super().assertEqual('{}', i._translate(0, T, T))

        # Feature symbol to specific symbol
        i.grammar = {F: [ORTH]}
        super().assertEqual('{<ORTH>}', i._translate(0, F, '{<F>}'))

        # Basic Terminal conversion
        i.grammar = {ORTH: ['Test']}
        super().assertEqual('{"ORTH":"Test"}', i._translate(0, ORTH, '{<ORTH>}'))

        # Underscore conversion
        i.grammar = {UNDERSCORE: [IS_CURRENCY]}
        super().assertEqual('{"_": {<CUSTOM_IS_CURRENCY>}}', i._translate(0, UNDERSCORE, '{<UNDERSCORE>}'))

        # Underscore terminal conversion
        i.grammar = {IS_CURRENCY: [True]}
        super().assertEqual('{"_": {"CUSTOM_IS_CURRENCY":"True"}}',
                            i._translate(0, IS_CURRENCY, '{"_": {<CUSTOM_IS_CURRENCY>}}'))

        # Grammar Operators conversion
        i.grammar = {OP: ZERO_OR_MORE}
        super().assertEqual('"OP":"*"', i._translate(0, OP, '<OP>'))

        # Extended Pattern Syntax conversion (base)
        i.grammar = {XPS: [IN]}
        super().assertEqual('{<IN>}', i._translate(0, XPS, '<XPS>'))

        i.grammar = {ORTH: [XPS]}
        super().assertEqual('"ORTH":<XPS>', i._translate(0, ORTH, '<ORTH>'))

        # Extended Pattern Syntax conversion (terminal logical)
        i.grammar = {NOT_IN: [['Test']]}
        super().assertEqual('{"ORTH": {"NOT_IN":["Test"]}}', i._translate(0, NOT_IN, '{"ORTH": {<NOT_IN>}}'))

        # Extended Pattern Syntax (terminal arithmetical)
        i.grammar = {GTH: [5]}
        super().assertEqual('{"LENGTH": {">":5}}', i._translate(0, GTH, '{"LENGTH": {<GTH>}}'))

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

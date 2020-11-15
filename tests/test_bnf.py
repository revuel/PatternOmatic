""" Unit testing file for BNF module

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
from spacy.tokens.doc import Underscore

import PatternOmatic.nlp.bnf as bnf
from PatternOmatic.settings.literals import S, P, T, F, OP, NEGATION, ZERO_OR_ONE, ZERO_OR_MORE, ONE_OR_MORE, XPS, IN,\
    NOT_IN, EQQ, GEQ, LEQ, GTH, LTH, TOKEN_WILDCARD, UNDERSCORE, ORTH, TEXT, LOWER, POS, TAG, DEP, LEMMA, SHAPE, \
    IS_ASCII, IS_UPPER, HAS_VECTOR
from PatternOmatic.settings.config import Config


class TestDG(unittest.TestCase):
    """ Test class for Dynamic Grammar """

    nlp = spacy.load('en_core_web_sm')
    samples = [nlp(u'This is a test.'), nlp(u'Checks for Backus Naur Form grammars')]
    config = None

    def test_basic_grammar_dg(self):
        """ Tests that basic grammar is correctly generated """
        grammar = bnf.dynamic_generator(self.samples)

        super().assertIn(P, grammar.keys())
        super().assertIn(S, grammar.keys())
        super().assertIn(T, grammar.keys())
        super().assertIn(F, grammar.keys())
        super().assertEqual(len(grammar[SHAPE]), 7)
        super().assertEqual(len(grammar[F]), 9)

    def test_basic_grammar_without_uniques_dg(self):
        """ Tests that basic grammar is correctly generated when use uniques is false """
        self.config.use_uniques = False
        grammar = bnf.dynamic_generator(self.samples)

        super().assertEqual(len(grammar[SHAPE]), 11)

    def test_basic_grammar_with_booleans_dg(self):
        """ Tests that basic grammar with booleans is correctly generated """
        self.config.use_boolean_features = True
        grammar = bnf.dynamic_generator(self.samples)

        super().assertIn(IS_ASCII, grammar.keys())
        super().assertIn(IS_UPPER, grammar.keys())

    def test_basic_grammar_with_booleans_and_operators_dg(self):
        """ Tests that basic grammar with boolean features and operators is correctly generated """
        self.config.use_boolean_features = True
        self.config.use_grammar_operators = True

        grammar = bnf.dynamic_generator(self.samples)

        super().assertIn(IS_ASCII, grammar.keys())
        super().assertIn(IS_UPPER, grammar.keys())
        super().assertIn(OP, grammar.keys())
        super().assertListEqual(grammar[OP], [NEGATION, ZERO_OR_ONE, ONE_OR_MORE, ZERO_OR_MORE])

    def test_basic_grammar_with_booleans_and_extended_pattern_syntax_dg(self):
        """ Tests that basic grammar with boolean features and extended pattern syntax is correctly generated """
        self.config.use_boolean_features = True
        self.config.use_extended_pattern_syntax = True

        grammar = bnf.dynamic_generator(self.samples)

        super().assertIn(IS_ASCII, grammar.keys())
        super().assertIn(IS_UPPER, grammar.keys())
        super().assertIn(XPS, grammar.keys())
        super().assertListEqual(grammar[XPS], [IN, NOT_IN, EQQ, GEQ, LEQ, GTH, LTH])

    def test_basic_grammar_with_booleans_and_custom_attributes_dg(self):
        """ Tests that basic grammar with boolean features and custom attributes is correctly generated  """
        self.config.use_boolean_features = True
        self.config.use_custom_attributes = True

        grammar = bnf.dynamic_generator(self.samples)

        super().assertIn(IS_ASCII, grammar.keys())
        super().assertIn(IS_UPPER, grammar.keys())
        super().assertIn(UNDERSCORE, grammar.keys())
        # super().assertIn(IS_SENT_START, grammar.keys())
        super().assertIn(HAS_VECTOR, grammar.keys())

    def test_basic_grammar_with_token_wildcard_dg(self):
        """ Tests grammar is generated with token wildcard """
        self.config.use_token_wildcard = True

        grammar = bnf.dynamic_generator(self.samples)

        super().assertIn(TOKEN_WILDCARD, grammar[T])

    def test_get_features_per_token(self):
        """ Tests that the number of features per token is properly set given different configurations """
        features_dict = {ORTH: None, TEXT: None, LOWER: None, POS: None, TAG: None, LEMMA: None}
        len_features_dict = len(features_dict.keys())

        # When features_per_token is equal or lower to 0, the maximum number of features per token is set
        self.config.features_per_token = 0
        super().assertEqual(len_features_dict, bnf._get_features_per_token(features_dict))
        self.config.features_per_token = -100
        super().assertEqual(len_features_dict, bnf._get_features_per_token(features_dict))

        # When features_per_token is greater than the actual features, the maximum number of features per token is set
        self.config.features_per_token = 100
        super().assertEqual(len_features_dict, bnf._get_features_per_token(features_dict))

        # When features_per_token is inside the range (0, actual features), the config parameter is respected
        self.config.features_per_token = 3
        super().assertEqual(3, bnf._get_features_per_token(features_dict))

    def test_symbol_stacker(self):
        """ Tests that symbols are stacked properly """
        expected_1 = [DEP, DEP + ',' + DEP, DEP + ',' + DEP + ',' + DEP]
        super().assertListEqual(expected_1, bnf._symbol_stacker(DEP, 3))

        expected_2 = [DEP + ',' + DEP,
                      DEP + ',' + DEP + ',' + DEP,
                      DEP + ',' + DEP + ',' + DEP + ',' + DEP]

        super().assertListEqual(expected_2, bnf._symbol_stacker(DEP, 4, 2))

        expected_2.insert(0, DEP)

        super().assertListEqual(expected_2, bnf._symbol_stacker(DEP, 4, 5))

        super().assertListEqual([expected_1[2]], bnf._symbol_stacker(DEP, 3, 3))

    #
    # Helpers
    #
    def setUp(self) -> None:
        """ Fresh Config instance """
        self.config = Config()

    def tearDown(self) -> None:
        """ Destroy Config instance, reset Underscore's token extensions """
        Config.clear_instance()
        Underscore.token_extensions = {}


if __name__ == "__main__":
    unittest.main()

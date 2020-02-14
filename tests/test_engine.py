""" Unit testing file for DG Engine """
import unittest
import spacy
from nlp.engine import dynagg
from settings.literals import *
from settings.config import Config

config = Config()


class TestDG(unittest.TestCase):
    """ Test class for Dynamic Grammar """

    nlp = spacy.load("en_core_web_sm")

    def test_basic_grammar_dg(self):
        """ Tests that basic grammar is correctly generated """
        config.features_per_token = 1
        self._aux_config_to_false()
        config.use_uniques = True

        samples = [self.nlp(u'This is a test.'), self.nlp(u'Checks for Backus Naur Form grammars')]
        grammar = dynagg(samples)

        assert S in grammar.keys()
        assert T in grammar.keys()
        assert F in grammar.keys()
        assert len(grammar[SHAPE]) == 7
        assert len(grammar[F]) == 10

    def test_basic_grammar_without_uniques_dg(self):
        """ Tests that basic grammar is correctly generated is correctly generated """
        config.features_per_token = 1
        self._aux_config_to_false()

        samples = [self.nlp(u'This is a test.'), self.nlp(u'Checks for Backus Naur Form grammars')]
        grammar = dynagg(samples)

        assert len(grammar[SHAPE]) == 11

    def test_basic_grammar_with_booleans_dg(self):
        """ Tests that basic grammar with booleans is correctly generated """
        config.features_per_token = 1
        self._aux_config_to_false()
        config.use_boolean_features = True

        samples = [self.nlp(u'This is a test.'), self.nlp(u'Checks for Backus Naur Form grammars')]
        grammar = dynagg(samples)

        assert IS_ASCII in grammar.keys()
        assert IS_UPPER in grammar.keys()

    def test_basic_grammar_with_booleans_and_operators_dg(self):
        """ Tests that basic grammar with boolean features and operators is correctly generated """
        config.features_per_token = 1
        self._aux_config_to_false()
        config.use_boolean_features = True
        config.use_grammar_operators = True

        samples = [self.nlp(u'This is a test.'), self.nlp(u'Checks for Backus Naur Form grammars')]
        grammar = dynagg(samples)

        assert IS_ASCII in grammar.keys()
        assert IS_UPPER in grammar.keys()
        assert OP in grammar.keys()
        assert grammar[OP] == ['!', '?', '+', '*']

    def test_basic_grammar_with_booleans_and_extended_pattern_syntax_dg(self):
        """ Tests that basic grammar with boolean features and extended pattern syntaxt is correctly generated """
        config.features_per_token = 1
        self._aux_config_to_false()
        config.use_boolean_features = True
        config.use_extended_pattern_syntax = True

        samples = [self.nlp(u'This is a test.'), self.nlp(u'Checks for Backus Naur Form grammars')]
        grammar = dynagg(samples)

        assert IS_ASCII in grammar.keys()
        assert IS_UPPER in grammar.keys()
        assert XPS in grammar.keys()
        assert grammar[XPS] == [IN, NOT_IN, EQQ, GEQ, LEQ, GTH, LTH]

    def test_basic_grammar_with_booleans_and_custom_attributes_dg(self):
        """ Tests that basic grammar with boolean features and custom attributes is correctly generated  """
        config.features_per_token = 1
        self._aux_config_to_false()
        config.use_boolean_features = True
        config.use_custom_attributes = True

        samples = [self.nlp(u'This is a test.'), self.nlp(u'Checks for Backus Naur Form grammars')]
        grammar = dynagg(samples)

        assert IS_ASCII in grammar.keys()
        assert IS_UPPER in grammar.keys()
        assert UNDERSCORE in grammar.keys()
        assert IS_SENT_START in grammar.keys()

    @staticmethod
    def _aux_config_to_false():
        """ Auxiliary method to set grammar config values to False """
        config.use_uniques = False
        config.use_boolean_features = False
        config.use_grammar_operators = False
        config.use_extended_pattern_syntax = False
        config.use_custom_attributes = False
        config.use_token_wildcard = False


if __name__ == "__main__":
    unittest.main()


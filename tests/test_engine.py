""" Unit testing file for DG Engine """
import unittest
import spacy
import gc
from spacy.tokens.doc import Underscore

from PatternOmatic.nlp.engine import dynagg
from PatternOmatic.settings.literals import *
from PatternOmatic.settings.config import Config


class TestDG(unittest.TestCase):
    """ Test class for Dynamic Grammar """

    nlp = spacy.load('en_core_web_sm')
    config = None

    def test_basic_grammar_dg(self):
        """ Tests that basic grammar is correctly generated """
        samples = [self.nlp(u'This is a test.'), self.nlp(u'Checks for Backus Naur Form grammars')]
        grammar = dynagg(samples)

        super().assertIn(S, grammar.keys())
        super().assertIn(T, grammar.keys())
        super().assertIn(F, grammar.keys())
        super().assertEqual(len(grammar[SHAPE]), 7)
        super().assertEqual(len(grammar[F]), 10)

    def test_basic_grammar_without_uniques_dg(self):
        """ Tests that basic grammar is correctly generated when use uniques is false """
        self.config.use_uniques = False

        samples = [self.nlp(u'This is a test.'), self.nlp(u'Checks for Backus Naur Form grammars')]
        grammar = dynagg(samples)

        super().assertEqual(len(grammar[SHAPE]), 11)

    def test_basic_grammar_with_booleans_dg(self):
        """ Tests that basic grammar with booleans is correctly generated """
        self.config.use_boolean_features = True

        samples = [self.nlp(u'This is a test.'), self.nlp(u'Checks for Backus Naur Form grammars')]
        grammar = dynagg(samples)

        super().assertIn(IS_ASCII, grammar.keys())
        super().assertIn(IS_UPPER, grammar.keys())

    def test_basic_grammar_with_booleans_and_operators_dg(self):
        """ Tests that basic grammar with boolean features and operators is correctly generated """
        self.config.use_boolean_features = True
        self.config.use_grammar_operators = True

        samples = [self.nlp(u'This is a test.'), self.nlp(u'Checks for Backus Naur Form grammars')]
        grammar = dynagg(samples)

        super().assertIn(IS_ASCII, grammar.keys())
        super().assertIn(IS_UPPER, grammar.keys())
        super().assertIn(OP, grammar.keys())
        super().assertListEqual(grammar[OP], ['!', '?', '+', '*'])

    def test_basic_grammar_with_booleans_and_extended_pattern_syntax_dg(self):
        """ Tests that basic grammar with boolean features and extended pattern syntaxt is correctly generated """
        self.config.use_boolean_features = True
        self.config.use_extended_pattern_syntax = True

        samples = [self.nlp(u'This is a test.'), self.nlp(u'Checks for Backus Naur Form grammars')]
        grammar = dynagg(samples)

        super().assertIn(IS_ASCII, grammar.keys())
        super().assertIn(IS_UPPER, grammar.keys())
        super().assertIn(XPS, grammar.keys())
        super().assertListEqual(grammar[XPS], [IN, NOT_IN, EQQ, GEQ, LEQ, GTH, LTH])

    def test_basic_grammar_with_booleans_and_custom_attributes_dg(self):
        """ Tests that basic grammar with boolean features and custom attributes is correctly generated  """
        self.config.use_boolean_features = True
        self.config.use_custom_attributes = True

        samples = [self.nlp(u'This is a test.'), self.nlp(u'Checks for Backus Naur Form grammars')]
        grammar = dynagg(samples)

        super().assertIn(IS_ASCII, grammar.keys())
        super().assertIn(IS_UPPER, grammar.keys())
        super().assertIn(UNDERSCORE, grammar.keys())
        # super().assertIn(IS_SENT_START, grammar.keys())

    def test_basic_grammar_with_token_wildcard_dg(self):
        """ Tests grammar is generated with token wildcard """
        self.config.use_token_wildcard = True

        samples = [self.nlp(u'This is a test.'), self.nlp(u'Checks for Backus Naur Form grammars')]
        grammar = dynagg(samples)

        super().assertIn(TOKEN_WILDCARD, grammar[T])

    def setUp(self) -> None:
        self.config = Config()

    def tearDown(self) -> None:
        Config.clear_instance()
        Underscore.token_extensions = {}


if __name__ == "__main__":
    unittest.main()

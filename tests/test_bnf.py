""" Unit testing file for DG Engine """
import unittest
import spacy
from spacy.tokens.doc import Underscore

from PatternOmatic.nlp.bnf import dynamic_generator
from PatternOmatic.settings.literals import S, P, T, F, OP, NEGATION, ZERO_OR_ONE, ZERO_OR_MORE, ONE_OR_MORE, LENGTH, \
    XPS, IN, NOT_IN, EQQ, GEQ, LEQ, GTH, LTH, TOKEN_WILDCARD, UNDERSCORE, EF, ORTH, TEXT, LOWER, POS, TAG, DEP, LEMMA, \
    SHAPE, ENT_TYPE, IS_ALPHA, IS_ASCII, IS_DIGIT, IS_BRACKET, IS_LOWER, IS_PUNCT, IS_QUOTE, IS_SPACE, IS_TITLE, \
    IS_OOV, IS_UPPER, IS_STOP, IS_CURRENCY, IS_LEFT_PUNCT, IS_RIGHT_PUNCT, IS_SENT_START, LIKE_NUM, LIKE_EMAIL, \
    LANG, NORM, PREFIX, SENTIMENT, STRING, SUFFIX, TEXT_WITH_WS, WHITESPACE, LIKE_URL, MATCHER_SUPPORTED_ATTRIBUTES, \
    ENT_ID, ENT_IOB, ENT_KB_ID, HAS_VECTOR, PROB
from PatternOmatic.settings.config import Config


class TestDG(unittest.TestCase):
    """ Test class for Dynamic Grammar """

    nlp = spacy.load('en_core_web_sm')
    samples = [nlp(u'This is a test.'), nlp(u'Checks for Backus Naur Form grammars')]
    config = None

    def test_basic_grammar_dg(self):
        """ Tests that basic grammar is correctly generated """
        grammar = dynamic_generator(self.samples)

        super().assertIn(P, grammar.keys())
        super().assertIn(S, grammar.keys())
        super().assertIn(T, grammar.keys())
        super().assertIn(F, grammar.keys())
        super().assertEqual(len(grammar[SHAPE]), 7)
        super().assertEqual(len(grammar[F]), 10)

    def test_basic_grammar_without_uniques_dg(self):
        """ Tests that basic grammar is correctly generated when use uniques is false """
        self.config.use_uniques = False
        grammar = dynamic_generator(self.samples)

        super().assertEqual(len(grammar[SHAPE]), 11)

    def test_basic_grammar_with_booleans_dg(self):
        """ Tests that basic grammar with booleans is correctly generated """
        self.config.use_boolean_features = True
        grammar = dynamic_generator(self.samples)

        super().assertIn(IS_ASCII, grammar.keys())
        super().assertIn(IS_UPPER, grammar.keys())

    def test_basic_grammar_with_booleans_and_operators_dg(self):
        """ Tests that basic grammar with boolean features and operators is correctly generated """
        self.config.use_boolean_features = True
        self.config.use_grammar_operators = True

        grammar = dynamic_generator(self.samples)

        super().assertIn(IS_ASCII, grammar.keys())
        super().assertIn(IS_UPPER, grammar.keys())
        super().assertIn(OP, grammar.keys())
        super().assertListEqual(grammar[OP], [NEGATION, ZERO_OR_ONE, ONE_OR_MORE, ZERO_OR_MORE])

    def test_basic_grammar_with_booleans_and_extended_pattern_syntax_dg(self):
        """ Tests that basic grammar with boolean features and extended pattern syntax is correctly generated """
        self.config.use_boolean_features = True
        self.config.use_extended_pattern_syntax = True

        grammar = dynamic_generator(self.samples)

        super().assertIn(IS_ASCII, grammar.keys())
        super().assertIn(IS_UPPER, grammar.keys())
        super().assertIn(XPS, grammar.keys())
        super().assertListEqual(grammar[XPS], [IN, NOT_IN, EQQ, GEQ, LEQ, GTH, LTH])

    def test_basic_grammar_with_booleans_and_custom_attributes_dg(self):
        """ Tests that basic grammar with boolean features and custom attributes is correctly generated  """
        self.config.use_boolean_features = True
        self.config.use_custom_attributes = True

        grammar = dynamic_generator(self.samples)

        super().assertIn(IS_ASCII, grammar.keys())
        super().assertIn(IS_UPPER, grammar.keys())
        super().assertIn(UNDERSCORE, grammar.keys())
        # super().assertIn(IS_SENT_START, grammar.keys())
        super().assertIn(HAS_VECTOR, grammar.keys())

    def test_basic_grammar_with_token_wildcard_dg(self):
        """ Tests grammar is generated with token wildcard """
        self.config.use_token_wildcard = True

        grammar = dynamic_generator(self.samples)

        super().assertIn(TOKEN_WILDCARD, grammar[T])

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

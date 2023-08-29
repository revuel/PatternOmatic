""" Literals/constants module

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
from enum import Enum, unique


#
# GE Related literals
#
@unique
class SelectionType(Enum):
    """ Evolutionary selection types """
    BINARY_TOURNAMENT = 0
    K_TOURNAMENT = 1

    def __repr__(self):
        """ Human readable """
        return self.name


@unique
class RecombinationType(Enum):
    """ Evolutionary recombination types enum """
    RANDOM_ONE_POINT_CROSSOVER = 0

    def __repr__(self):
        """ Human readable """
        return self.name


@unique
class ReplacementType(Enum):
    """ Evolutionary replacement types enum """
    MU_PLUS_LAMBDA = 0
    MU_LAMBDA_WITH_ELITISM = 1
    MU_LAMBDA_WITHOUT_ELITISM = 2

    def __repr__(self):
        """ Human readable """
        return self.name


# Fitness types
@unique
class FitnessType(Enum):
    """ Fitness function type """
    BASIC = 0
    FULL_MATCH = 1

    def __repr__(self):
        """ Human readable """
        return self.name


#
# Dynamic grammar generation related literals
#
# Symbol delimiters
SLD = '<'
SRD = '>'
# Grammar symbols
S = SLD + 'S' + SRD
P = SLD + 'P' + SRD
T = SLD + 'T' + SRD
F = SLD + 'F' + SRD
# Feature symbols (base)
ORTH = SLD + 'ORTH' + SRD
TEXT = SLD + 'TEXT' + SRD
LOWER = SLD + 'LOWER' + SRD
LENGTH = SLD + 'LENGTH' + SRD
POS = SLD + 'POS' + SRD
TAG = SLD + 'TAG' + SRD
DEP = SLD + 'DEP' + SRD
LEMMA = SLD + 'LEMMA' + SRD
SHAPE = SLD + 'SHAPE' + SRD
ENT_TYPE = SLD + 'ENT_TYPE' + SRD
# Feature symbols (base boolean)
IS_ALPHA = SLD + 'IS_ALPHA' + SRD
IS_ASCII = SLD + 'IS_ASCII' + SRD
IS_DIGIT = SLD + 'IS_DIGIT' + SRD
IS_LOWER = SLD + 'IS_LOWER' + SRD
IS_UPPER = SLD + 'IS_UPPER' + SRD
IS_TITLE = SLD + 'IS_TITLE' + SRD
IS_PUNCT = SLD + 'IS_PUNCT' + SRD
IS_SPACE = SLD + 'IS_SPACE' + SRD
IS_STOP = SLD + 'IS_STOP' + SRD
LIKE_NUM = SLD + 'LIKE_NUM' + SRD
LIKE_URL = SLD + 'LIKE_URL' + SRD
LIKE_EMAIL = SLD + 'LIKE_EMAIL' + SRD
# Grammar operator and quantifier symbols
OP = SLD + 'OP' + SRD
NEGATION = '!'
ZERO_OR_ONE = '?'
ONE_OR_MORE = '+'
ZERO_OR_MORE = '*'
# Token wildcard
TOKEN_WILDCARD = '{}'
# Grammar extended pattern syntax
XPS = SLD + 'XPS' + SRD
IN = SLD + 'IN' + SRD
NOT_IN = SLD + 'NOT_IN' + SRD
EQQ = SLD + 'EQQ' + SRD
GEQ = SLD + 'GEQ' + SRD
LEQ = SLD + 'LEQ' + SRD
GTH = SLD + 'GTH' + SRD
LTH = SLD + 'LTH' + SRD
XPS_AS = {EQQ: "==", GEQ: ">=", LEQ: "<=", GTH: ">", LTH: "<"}
# Grammar custom attributes extension symbol
UNDERSCORE = SLD + 'UNDERSCORE' + SRD
EF = SLD + 'EF' + SRD
ENT_ID = SLD + 'CUSTOM_ENT_ID_' + SRD
ENT_IOB = SLD + 'CUSTOM_ENT_IOB_' + SRD
ENT_KB_ID = SLD + 'CUSTOM_ENT_KB_ID_' + SRD
HAS_VECTOR = SLD + 'CUSTOM_HAS_VECTOR' + SRD
IS_BRACKET = SLD + 'CUSTOM_IS_BRACKET' + SRD
IS_CURRENCY = SLD + 'CUSTOM_IS_CURRENCY' + SRD
IS_LEFT_PUNCT = SLD + 'CUSTOM_IS_LEFT_PUNCT' + SRD
IS_OOV = SLD + 'CUSTOM_IS_OOV' + SRD
IS_QUOTE = SLD + 'CUSTOM_IS_QUOTE' + SRD
IS_RIGHT_PUNCT = SLD + 'CUSTOM_IS_RIGHT_PUNCT' + SRD
IS_SENT_START = SLD + 'CUSTOM_IS_SENT_START' + SRD
LANG = SLD + 'CUSTOM_LANG_' + SRD
NORM = SLD + 'CUSTOM_NORM_' + SRD
PREFIX = SLD + 'CUSTOM_PREFIX_' + SRD
PROB = SLD + 'CUSTOM_PROB' + SRD
SENT_START = SLD + 'CUSTOM_SENT_START' + SRD
SENTIMENT = SLD + 'CUSTOM_SENTIMENT' + SRD
STRING = SLD + 'CUSTOM_STRING' + SRD
SUFFIX = SLD + 'CUSTOM_SUFFIX_' + SRD
TEXT_WITH_WS = SLD + 'CUSTOM_TEXT_WITH_WS' + SRD
WHITESPACE = SLD + 'CUSTOM_WHITESPACE_' + SRD
# Matcher's util
MATCHER_SUPPORTED_ATTRIBUTES = (
    'orth_',
    'text',
    'lower_',
    'pos_',
    'tag_',
    'dep_',
    'lemma_',
    'shape_',
    'ent_type_',
    'is_alpha',
    'is_ascii',
    'is_digit',
    'is_lower',
    'is_upper',
    'is_title',
    'is_punct',
    'is_space',
    'is_stop',
    'like_num',
    'like_url',
    'like_email')

#
# Config ini literals
#
GE = 'GE'
MAX_RUNS = 'MAX_RUNS'
SUCCESS_THRESHOLD = 'SUCCESS_THRESHOLD'
POPULATION_SIZE = 'POPULATION_SIZE'
MAX_GENERATIONS = 'MAX_GENERATIONS'
CODON_LENGTH = 'CODON_LENGTH'
CODONS_X_INDIVIDUAL = 'CODONS_X_INDIVIDUAL'
MUTATION_PROBABILITY = 'MUTATION_PROBABILITY'
OFFSPRING_FACTOR = 'OFFSPRING_FACTOR'
MATING_PROBABILITY = 'MATING_PROBABILITY'
K_VALUE = 'K_VALUE'
SELECTION_TYPE = 'SELECTION_TYPE'
RECOMBINATION_TYPE = 'RECOMBINATION_TYPE'
REPLACEMENT_TYPE = 'REPLACEMENT_TYPE'
FITNESS_FUNCTION_TYPE = 'FITNESS_FUNCTION_TYPE'
DGG = 'DGG'
FEATURES_X_TOKEN = 'FEATURES_X_TOKEN'
USE_BOOLEAN_FEATURES = 'USE_BOOLEAN_FEATURES'
USE_UNIQUES = 'USE_UNIQUES'
USE_GRAMMAR_OPERATORS = 'USE_GRAMMAR_OPERATORS'
USE_TOKEN_WILDCARD = 'USE_TOKEN_WILDCARD'
USE_EXTENDED_PATTERN_SYNTAX = 'USE_EXTENDED_PATTERN_SYNTAX'
USE_CUSTOM_ATTRIBUTES = 'USE_CUSTOM_ATTRIBUTES'
IO = 'IO'
REPORT_PATH = 'REPORT_PATH'
REPORT_FORMAT = 'REPORT_FORMAT'


@unique
class ReportFormat(Enum):
    """ Report format type """
    JSON = 0
    CSV = 1

    def __repr__(self):
        """ Human readable """
        return self.name

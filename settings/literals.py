""" Literals & constants module """

''' GE Related literals '''
# Selection types
BINARY_TOURNAMENT = 'Binary tournament'
K_TOURNAMENT = 'K tournament'
# Recombination types
RANDOM_ONE_POINT_CROSSOVER = 'Random one point crossover'
# Replacement types
MU_PLUS_LAMBDA = 'Mu plus lambda'
MU_LAMBDA_WITH_ELITISM = 'Mu lambda with elitism'
MU_LAMBDA_WITHOUT_ELITISM = 'Mu lambda without elitism'
# Fitness types
FITNESS_BASIC = 'Basic fitness function'
FITNESS_FULLMATCH = 'Fullmatch fitness function'

''' Dynamic grammar generation related literals '''
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
ENT = SLD + 'ENT' + SRD
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
MATCHER_SUPPORTED_ATTRIBUTES =  ('orth_', 'text', 'lower_', 'pos_', 'tag_', 'dep_', 'lemma_', 'shape_', 'is_alpha',
                                 'is_ascii', 'is_digit', 'is_lower', 'is_upper', 'is_title', 'is_punct', 'is_space',
                                 'is_stop', 'like_num', 'like_url', 'like_email')
''' Config ini literals '''
GE = 'GE'
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
DGG = 'DGG'
FEATURES_X_TOKEN = 'FEATURES_X_TOKEN'
USE_BOOLEAN_FEATURES = 'USE_BOOLEAN_FEATURES'
USE_UNIQUES = 'USE_UNIQUES'
USE_GRAMMAR_OPERATORS = 'USE_GRAMMAR_OPERATORS'
USE_TOKEN_WILDCARD = 'USE_TOKEN_WILDCARD'
USE_EXTENDED_PATTERN_SYNTAX = 'USE_EXTENDED_PATTERN_SYNTAX'
USE_CUSTOM_ATTRIBUTES = 'USE_CUSTOM_ATTRIBUTES'
FITNESS_FUNCTION_TYPE = 'FITNESS_FUNCTION_TYPE'


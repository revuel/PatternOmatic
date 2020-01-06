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

''' Dynamic grammar generation related literals '''
# Symbol delimiters
SLD = '<'
SRD = '>'
# Grammar symbols
S = SLD + 'S' + SRD
P = SLD + 'P' + SRD
T = SLD + 'T' + SRD
F = SLD + 'F' + SRD
# Feature symbols
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
# Grammar token operator symbols
OP = SLD + 'OP' + SRD
NEGATION = '!'
ZERO_OR_ONE = '?'
ONE_OR_MORE = '+'
ZERO_OR_MORE = '*'
# Token wildcard
TOKEN_WILDCARD = '{}'

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
USE_CUSTOM_FEATURES = 'USE_CUSTOM_FEATURES'
USE_UNIQUES = 'USE_UNIQUES'
USE_GRAMMAR_OPERATORS = 'USE_GRAMMAR_OPERATORS'
USE_TOKEN_WILDCARD = 'USE_TOKEN_WILDCARD'
FITNESS_FUNCTION_TYPE = 'FITNESS_FUNCTION_TYPE'

""" Literals file """

''' GE Related literals '''
# Selection
BINARY_TOURNAMENT = 'Binary tournament'
K_TOURNAMENT = 'K tournament'
# Recombination
RANDOM_ONE_POINT_CROSSOVER = 'Random one point crossover'
# Replacement
MU_PLUS_LAMBDA = 'Mu plus lambda'
MU_LAMBDA_WITH_ELITISM = 'Mu lambda with elitism'
MU_LAMBDA_WITHOUT_ELITISM = 'Mu lambda without elitism'
# Fitness
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

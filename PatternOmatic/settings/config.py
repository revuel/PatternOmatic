""" Configuration Management class """
from __future__ import annotations
from typing import Optional
from PatternOmatic.settings.literals import *
import configparser
import logging


def str2bool(vargin: str) -> bool:
    """
    Auxiliary method to parse boolean configuration file options
    Args:
        vargin: argument to evaluate

    Returns: True if v in string set, False otherwise

    """
    return vargin.lower() in ('Yes', 'yes', 'True', 'true', '1')


class SingletonMetaNaive(type):
    """ The Naive Singleton Design Pattern of type Metaclass builder """

    _instance: Optional[Config] = None

    def __call__(cls) -> Config:
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance


class Config(metaclass=SingletonMetaNaive):
    """ Singleton Configuration Class for PatternOmatic package """
    def __init__(self):
        """ Config object constructor """
        try:
            config_parser = configparser.ConfigParser()
            file_list = config_parser.read('config.ini')

            if len(file_list) == 0:
                raise FileNotFoundError

            # GE configuration parameters
            self._max_runs = int(config_parser[GE][MAX_RUNS])
            self._success_threshold = float(config_parser[GE][SUCCESS_THRESHOLD])
            self._population_size = int(config_parser[GE][POPULATION_SIZE])
            self._max_generations = int(config_parser[GE][MAX_GENERATIONS])
            self._codon_length = int(config_parser[GE][CODON_LENGTH])
            self._num_codons_per_individual = int(config_parser[GE][CODONS_X_INDIVIDUAL])
            self._dna_length = self._codon_length * self._num_codons_per_individual
            self._mutation_probability = float(config_parser[GE][MUTATION_PROBABILITY])
            self._offspring_max_size_factor = float(config_parser[GE][OFFSPRING_FACTOR])
            self._mating_probability = float(config_parser[GE][MATING_PROBABILITY])
            self._k_value = int(config_parser[GE][K_VALUE])

            # GE configuration methods
            self._selection_type = globals()[config_parser[GE][SELECTION_TYPE]]
            self._recombination_type = globals()[config_parser[GE][RECOMBINATION_TYPE]]
            self._replacement_type = globals()[config_parser[GE][REPLACEMENT_TYPE]]

            # Dynamic Grammar Generation configuration options
            self._features_per_token = int(config_parser[DGG][FEATURES_X_TOKEN])
            self._use_boolean_features = str2bool(config_parser[DGG][USE_BOOLEAN_FEATURES])
            self._use_custom_attributes = str2bool(config_parser[DGG][USE_CUSTOM_ATTRIBUTES])
            self._use_uniques = str2bool(config_parser[DGG][USE_UNIQUES])
            self._use_grammar_operators = str2bool(config_parser[DGG][USE_GRAMMAR_OPERATORS])
            self._use_token_wildcard = str2bool(config_parser[DGG][USE_TOKEN_WILDCARD])
            self._use_extended_pattern_syntax = str2bool(config_parser[DGG][USE_EXTENDED_PATTERN_SYNTAX])

            # Problem specific configuration options
            self._fitness_function_type = globals()[config_parser[DGG][FITNESS_FUNCTION_TYPE]]

            # CONFIGURATION CHECKS (FILE ONLY)
            self._check_xps_op_restriction()

        except FileNotFoundError:
            logging.warning('Unable to locate config.ini file, using default configuration parameters')

            # GE configuration parameters
            self._max_runs = 1
            self._success_threshold = 0.8
            self._population_size = 10
            self._max_generations = 3
            self._codon_length = 8
            self._num_codons_per_individual = 4
            self._dna_length = self._codon_length * self._num_codons_per_individual
            self._mutation_probability = 0.5
            self._offspring_max_size_factor = 3.5
            self._mating_probability = 0.9
            self._k_value = 3

            # GE configuration methods
            self._selection_type = BINARY_TOURNAMENT
            self._recombination_type = RANDOM_ONE_POINT_CROSSOVER
            self._replacement_type = MU_PLUS_LAMBDA

            # Dynamic Grammar Generation configuration options
            self._features_per_token = 1
            self._use_boolean_features = False
            self._use_custom_attributes = False
            self._use_uniques = True
            self._use_grammar_operators = False
            self._use_token_wildcard = False
            self._use_extended_pattern_syntax = False

            # Problem specific configuration options
            self._fitness_function_type = FITNESS_FULLMATCH

    def __iter__(self):
        yield 'Number of runs', self.max_runs
        yield 'Success Threshold', self.success_threshold
        yield 'Population size', self.population_size
        yield 'Maximum number of generations', self.max_generations
        yield 'Codon length', self.codon_length
        yield 'Number of codons per Individual', self.num_codons_per_individual
        yield 'DNA length', self.dna_length
        yield 'Mutation probability', self.mutation_probability
        yield 'Offspring maximum size factor', self.offspring_max_size_factor
        yield 'Mating probability', self.mating_probability
        yield 'K tournament size value', self.k_value
        yield 'Selection algorithm', self.selection_type
        yield 'Recombination algorithm', self.recombination_type
        yield 'Replacement algorithm', self.replacement_type
        yield 'Maximum number of features per token', self.features_per_token
        yield 'Using boolean features?', self.use_boolean_features
        yield 'Using custom attributes?', self.use_custom_attributes
        yield 'Using unique feature terminal?', self.use_uniques
        yield 'Using grammar operators?', self.use_grammar_operators
        yield 'Using token wildcards?', self.use_token_wildcard
        yield 'Using extended pattern syntax?', self.use_extended_pattern_syntax
        yield 'Fitness function type', self.fitness_function_type

    @property
    def max_runs(self) -> int:
        return self._max_runs

    @property
    def success_threshold(self) -> float:
        return self._success_threshold

    @property
    def population_size(self) -> int:
        return self._population_size

    @population_size.setter
    def population_size(self, value: int) -> None:
        self.population_size = value

    @property
    def max_generations(self) -> int:
        return self._max_generations

    @max_generations.setter
    def max_generations(self, value: int) -> None:
        self._max_generations = value

    @property
    def codon_length(self) -> int:
        return self._codon_length

    @codon_length.setter
    def codon_length(self, value) -> None:
        self.codon_length = value

    @property
    def num_codons_per_individual(self) -> int:
        return self._num_codons_per_individual

    @num_codons_per_individual.setter
    def num_codons_per_individual(self, value: int) -> None:
        self.num_codons_per_individual = value

    @property
    def dna_length(self) -> int:
        return self._dna_length

    @property
    def mutation_probability(self) -> float:
        return self._mutation_probability

    @mutation_probability.setter
    def mutation_probability(self, value: float) -> None:
        self._mutation_probability = value

    @property
    def offspring_max_size_factor(self) -> float:
        return self._offspring_max_size_factor

    @property
    def mating_probability(self) -> float:
        return self._mating_probability

    @property
    def k_value(self) -> int:
        return self._k_value

    @property
    def selection_type(self) -> str:
        return self._selection_type

    @selection_type.setter
    def selection_type(self, value) -> None:
        self._selection_type = value

    @property
    def recombination_type(self) -> str:
        return self._recombination_type

    @recombination_type.setter
    def recombination_type(self, value) -> None:
        self._recombination_type = value

    @property
    def replacement_type(self) -> str:
        return self._replacement_type

    @replacement_type.setter
    def replacement_type(self, value) -> None:
        self._replacement_type = value

    @property
    def features_per_token(self) -> int:
        return self._features_per_token

    @features_per_token.setter
    def features_per_token(self, value: int) -> None:
        self._features_per_token = value

    @property
    def use_boolean_features(self) -> bool:
        return self._use_boolean_features

    @use_boolean_features.setter
    def use_boolean_features(self, value: int) -> None:
        self._use_boolean_features = value

    @property
    def use_custom_attributes(self) -> bool:
        return self._use_custom_attributes

    @use_custom_attributes.setter
    def use_custom_attributes(self, value: int) -> None:
        self._use_custom_attributes = value

    @property
    def use_uniques(self) -> bool:
        return self._use_uniques

    @use_uniques.setter
    def use_uniques(self, value: int) -> None:
        self._use_uniques = value

    @property
    def use_grammar_operators(self) -> bool:
        return self._use_grammar_operators

    @use_grammar_operators.setter
    def use_grammar_operators(self, value: int) -> None:
        self._use_grammar_operators = value

    @property
    def use_token_wildcard(self) -> bool:
        return self._use_token_wildcard

    @use_token_wildcard.setter
    def use_token_wildcard(self, value: bool) -> None:
        self._use_token_wildcard = value

    @property
    def use_extended_pattern_syntax(self) -> bool:
        return self._use_extended_pattern_syntax

    @use_extended_pattern_syntax.setter
    def use_extended_pattern_syntax(self, value) -> None:
        self._use_extended_pattern_syntax = value

    @property
    def fitness_function_type(self):
        return self._fitness_function_type

    @fitness_function_type.setter
    def fitness_function_type(self, value: int) -> None:
        self._fitness_function_type = value

    # Configuration restrictions
    def _check_xps_op_restriction(self):
        if self._use_extended_pattern_syntax == self._use_grammar_operators is True:
            logging.warning('Extended Pattern Syntax is not compatible with the usage of grammar operators')
            logging.warning('Extended Pattern Syntax has been disabled!')
            self._use_extended_pattern_syntax = False

    # Auxiliary methods
    def show(self):
        """ Prints current configuration in JSON format """
        return print(dict(self))

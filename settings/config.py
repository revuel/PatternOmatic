""" Configuration Management class """
from __future__ import annotations
from typing import Optional
from settings.literals import *
import configparser


def str2bool(vargin: str) -> bool:
    """
    Auxiliary method to parse boolean configuration file options
    Args:
        vargin: argument to evaluate

    Returns: True if v in string set, False otherwise

    """
    return vargin.lower() in ("yes", "True", "true", "1")


class SingletonMetaNaive(type):
    """ The Naive Singleton Design Pattern of type metaclass """

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

            ''' GE configuration parameters '''
            self._population_size = int(config_parser[GE][POPULATION_SIZE])
            self._max_generations = int(config_parser[GE][MAX_GENERATIONS])
            self._codon_length = int(config_parser[GE][CODON_LENGTH])
            self._num_codons_per_individual = int(config_parser[GE][CODONS_X_INDIVIDUAL])
            self._dna_length = self._codon_length * self._num_codons_per_individual
            self._mutation_probability = float(config_parser[GE][MUTATION_PROBABILITY])
            self._offspring_max_size_factor = float(config_parser[GE][OFFSPRING_FACTOR])
            self._mating_probability = float(config_parser[GE][MATING_PROBABILITY])
            self._k_value = int(config_parser[GE][K_VALUE])

            ''' GE configuration methods '''
            self._selection_type = globals()[config_parser[GE][SELECTION_TYPE]]
            self._recombination_type = globals()[config_parser[GE][RECOMBINATION_TYPE]]
            self._replacement_type = globals()[config_parser[GE][REPLACEMENT_TYPE]]

            ''' Dynamic Grammar Generation configuration options '''
            self._features_per_token = int(config_parser[DGG][FEATURES_X_TOKEN])
            self._extended_features = str2bool(config_parser[DGG][FEATURE_EXTENSION])
            self._use_uniques = str2bool(config_parser[DGG][USE_UNIQUES])
            self._use_grammar_operators = str2bool(config_parser[DGG][GRAMMAR_OPERATORS])
            self._token_wildcard = str2bool(config_parser[DGG][TOKEN_WILDCARD])

            ''' Problem specific configuration options '''
            self._fitness_function_type = globals()[config_parser[DGG][FITNESS_FUNCTION_TYPE]]

        except FileNotFoundError:
            print('Unable to locate config.ini file, using default configuration parameters')

            ''' GE configuration parameters '''
            self._population_size = 10
            self._max_generations = 3
            self._codon_length = 8
            self._num_codons_per_individual = 4
            self._dna_length = self._codon_length * self._num_codons_per_individual
            self._mutation_probability = 0.5
            self._offspring_max_size_factor = 3.5
            self._mating_probability = 0.9
            self._k_value = None

            ''' GE configuration methods '''
            self._selection_type = BINARY_TOURNAMENT
            self._recombination_type = RANDOM_ONE_POINT_CROSSOVER
            self._replacement_type = MU_PLUS_LAMBDA

            ''' Dynamic Grammar Generation configuration options '''
            self._features_per_token = 1
            self._extended_features = True
            self._use_uniques = True
            self._use_grammar_operators = False
            self._use_grammar_wildcards = False

            ''' Problem specific configuration options '''
            self._fitness_function_type = FITNESS_BASIC

    def __iter__(self):
        pass


if __name__ == "__main__":
    # The client code.

    s1 = Config()
    s2 = Config()

    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
        s1._population_size = 12
        print("Population Size S1:", s1._population_size)
        print("Population Size S2:", s2._population_size)
    else:
        print("Singleton failed, variables contain different instances.")

""" Configuration Management class """
from __future__ import annotations
from typing import Optional
from settings.literals import *
import configparser


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

        ''' GE configuration parameters '''
        self._population_size = 10
        self._max_generations = 300
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

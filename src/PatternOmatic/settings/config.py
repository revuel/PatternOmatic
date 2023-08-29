""" Configuration Management module

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
from __future__ import annotations
import configparser
from typing import Optional
from PatternOmatic.settings.log import LOG
from PatternOmatic.settings.literals import GE, MAX_RUNS, SUCCESS_THRESHOLD, POPULATION_SIZE, MAX_GENERATIONS, \
    CODON_LENGTH, CODONS_X_INDIVIDUAL, MUTATION_PROBABILITY, OFFSPRING_FACTOR, MATING_PROBABILITY, K_VALUE, \
    SELECTION_TYPE, REPLACEMENT_TYPE, RECOMBINATION_TYPE, RecombinationType, ReplacementType, SelectionType, \
    FitnessType, FITNESS_FUNCTION_TYPE, \
    DGG, FEATURES_X_TOKEN, USE_BOOLEAN_FEATURES, USE_CUSTOM_ATTRIBUTES, USE_UNIQUES, \
    USE_GRAMMAR_OPERATORS, USE_TOKEN_WILDCARD, USE_EXTENDED_PATTERN_SYNTAX, REPORT_PATH, IO, ReportFormat, REPORT_FORMAT


class SingletonMetaNaive(type):
    """ The Naive Singleton Design Pattern of type Metaclass builder """

    _instance: Optional[Config, None] = None

    def __call__(cls, config_file_path: str = None) -> Config:
        if cls._instance is None:
            LOG.debug('Creating config object!')
            cls._instance = super().__call__(config_file_path)
        return cls._instance

    def clear_instance(self):
        """ For testing purposes, destroy Singleton instance """
        LOG.debug('Removing config object!')
        self._instance = None
        del self._instance


class Config(metaclass=SingletonMetaNaive):
    """ Singleton Configuration package's Class"""
    __slots__ = (
        'max_runs',
        'success_threshold',
        'population_size',
        'max_generations',
        'codon_length',
        'num_codons_per_individual',
        'dna_length',
        'mutation_probability',
        'offspring_max_size_factor',
        'mating_probability',
        'k_value',
        'selection_type',
        'recombination_type',
        'replacement_type',
        'fitness_function_type',
        'features_per_token',
        'use_boolean_features',
        'use_custom_attributes',
        'use_uniques',
        'use_grammar_operators',
        'use_token_wildcard',
        'use_extended_pattern_syntax',
        'report_path',
        'report_format',
        'file_path'
    )

    def __init__(self, config_file_path: str = None):
        """
        Config object constructor
        Args:
            config_file_path: Path for a configuration file
        """
        config_parser = configparser.ConfigParser()

        if config_file_path is None:
            LOG.warning(f'Configuration file not provided. Falling back to default values')
            self.file_path = None
        else:
            file_list = config_parser.read(config_file_path)
            if len(file_list) == 0:
                LOG.warning(f'File {config_file_path} not found. Falling back to default values')
                self.file_path = None
            else:
                self.file_path = config_file_path

        #
        # GE configuration parameters
        #
        self.max_runs = self._validate_config_argument(GE, MAX_RUNS, 4, config_parser)
        self.success_threshold = self._validate_config_argument(GE, SUCCESS_THRESHOLD, 0.8, config_parser)
        self.population_size = self._validate_config_argument(GE, POPULATION_SIZE, 10, config_parser)
        self.max_generations = self._validate_config_argument(GE, MAX_GENERATIONS, 3, config_parser)
        self.codon_length = self._validate_config_argument(GE, CODON_LENGTH, 8, config_parser)
        self.num_codons_per_individual = self._validate_config_argument(GE, CODONS_X_INDIVIDUAL, 4, config_parser)
        self.dna_length = self.codon_length * self.num_codons_per_individual
        self.mutation_probability = self._validate_config_argument(GE, MUTATION_PROBABILITY, 0.5, config_parser)
        self.offspring_max_size_factor = self._validate_config_argument(GE, OFFSPRING_FACTOR, 3.5, config_parser)
        self.mating_probability = self._validate_config_argument(GE, MATING_PROBABILITY, 0.9, config_parser)
        self.k_value = self._validate_config_argument(GE, K_VALUE, 3, config_parser)

        #
        # GE configuration methods
        #
        self.selection_type = SelectionType(
            self._validate_config_argument(GE, SELECTION_TYPE, 0, config_parser))

        self.recombination_type = RecombinationType(
            self._validate_config_argument(GE, RECOMBINATION_TYPE, 0, config_parser))

        self.replacement_type = ReplacementType(
            self._validate_config_argument(GE, REPLACEMENT_TYPE, 0, config_parser))

        self.fitness_function_type = FitnessType(
            self._validate_config_argument(GE, FITNESS_FUNCTION_TYPE, 1, config_parser))

        #
        # BNF Grammar Generation configuration options
        #
        self.features_per_token = self._validate_config_argument(DGG, FEATURES_X_TOKEN, 1, config_parser)
        self.use_boolean_features = self._validate_config_argument(DGG, USE_BOOLEAN_FEATURES, False, config_parser)
        self.use_custom_attributes = self._validate_config_argument(DGG, USE_CUSTOM_ATTRIBUTES, False, config_parser)
        self.use_uniques = self._validate_config_argument(DGG, USE_UNIQUES, True, config_parser)
        self.use_grammar_operators = self._validate_config_argument(DGG, USE_GRAMMAR_OPERATORS, False, config_parser)
        self.use_token_wildcard = self._validate_config_argument(DGG, USE_TOKEN_WILDCARD, False, config_parser)
        self.use_extended_pattern_syntax = \
            self._validate_config_argument(DGG, USE_EXTENDED_PATTERN_SYNTAX, False, config_parser)

        #
        # Configuration validation
        #
        self._check_xps_op_restriction()

        #
        # IO
        #
        self.report_path = \
            self._validate_config_argument(IO, REPORT_PATH, '/tmp/patternomatic_report.txt', config_parser)

        self.report_format = ReportFormat(self._validate_config_argument(IO, REPORT_FORMAT, 0, config_parser))

        LOG.info(f'Configuration instance: {self}')

    def __setattr__(self, key, value) -> None:
        """
        Overrides method to be used with slots
        Args:
            key: An object slotted property
            value: An intended value for the object key

        Returns: None

        """
        if hasattr(self, key):
            if self._preserve_property_type(getattr(self, key), value):
                super(Config, self).__setattr__(key, value)
                LOG.info(f'Updating configuration parameter {key.upper()} with value {value}')
                if key == USE_EXTENDED_PATTERN_SYNTAX.lower() or key == USE_GRAMMAR_OPERATORS.lower():
                    self._check_xps_op_restriction()
            else:
                LOG.warning(f'Invalid data type {type(value)} for property {key}. Skipping update')
        else:
            super(Config, self).__setattr__(key, value)

    @property
    def __dict__(self):
        """ Hijacks dictionary for this config slotted class """
        return {s: getattr(self, s, None) for s in self.__slots__}

    def __repr__(self):
        """ Representation of config instance """
        return f'{self.__class__.__name__}({self.__dict__})'

    #
    # Utilities
    #
    @staticmethod
    def _validate_config_argument(section, option, default, config_parser):
        """

        Args:
            section:
            option:
            default:
            config_parser:

        Returns:

        """
        try:
            if isinstance(default, bool):
                value = config_parser.getboolean(section, option, fallback=default)
            elif isinstance(default, int):
                value = config_parser.getint(section, option, fallback=default)
            elif isinstance(default, float):
                value = config_parser.getfloat(section, option, fallback=default)
            elif isinstance(default, str):
                value = config_parser.get(section, option, fallback=default)
            else:
                value = default
        except ValueError:
            LOG.warning(f'[{section}][{option}] configuration parameter wrongly set. '
                        f'Falling back to its default value: {default}')
            value = default

        LOG.debug(f'[{section}][{option}] {value}')
        return value

    @staticmethod
    def _preserve_property_type(_property, value):
        return isinstance(value, type(_property))

    #
    # Problem specific restrictions
    #
    def _check_xps_op_restriction(self) -> None:
        """
        Spacy's Grammar Operators and Quantifiers and the Spacy's Extended Pattern Syntax can not be used together  at
        the same time in a pattern for the Spacy's Rule Based Matcher.

        This method checks the provided configuration and disables the Spacy's Extended Pattern Syntax if both
        mechanisms are found enabled at the provided configuration.

        Returns: None

        """
        if hasattr(self, USE_EXTENDED_PATTERN_SYNTAX.lower()) and hasattr(self, USE_GRAMMAR_OPERATORS.lower()) and \
                self.use_extended_pattern_syntax is True and self.use_grammar_operators is True:
            LOG.warning(f'Extended Pattern Syntax is not compatible with the usage of Grammar Operators. '
                        f'Extended Pattern Syntax has been disabled!')
            self.use_extended_pattern_syntax = False

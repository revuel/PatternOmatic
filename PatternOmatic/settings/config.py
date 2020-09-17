""" Configuration Management module """
from __future__ import annotations
import configparser
from typing import Optional
from PatternOmatic.settings.log import LOG
from PatternOmatic.settings.literals import *


class SingletonMetaNaive(type):
    """ The Naive Singleton Design Pattern of type Metaclass builder """

    _instance: Optional[Config, None] = None

    def __call__(cls, config_file_path: str = None) -> Config:
        if cls._instance is None:
            LOG.debug('Creating config object!')
            cls._instance = super().__call__(config_file_path)
        return cls._instance

    def clear_instance(self):
        LOG.debug('Removing config object!')
        self._instance = None
        del self._instance


class Config(metaclass=SingletonMetaNaive):
    """ Singleton Configuration Class for PatternOmatic package """
    def __init__(self, config_file_path: str = None):
        """
        Config object constructor
        Args:
            config_file_path: Path for a configuration file
        """
        config_parser = configparser.ConfigParser()

        if config_file_path is None:
            LOG.warning(f'Configuration file not provided. Falling back to default values')
        else:
            file_list = config_parser.read(config_file_path)
            if len(file_list) == 0:
                LOG.warning(f'File {config_file_path} not found. Falling back to default values')

        #
        # GE configuration parameters
        #
        self._max_runs = self._validate_config_argument(GE, MAX_RUNS, 4, config_parser)
        self._success_threshold = self._validate_config_argument(GE, SUCCESS_THRESHOLD, 0.8, config_parser)
        self._population_size = self._validate_config_argument(GE, POPULATION_SIZE, 10, config_parser)
        self._max_generations = self._validate_config_argument(GE, MAX_GENERATIONS, 3, config_parser)
        self._codon_length = self._validate_config_argument(GE, CODON_LENGTH, 8, config_parser)
        self._num_codons_per_individual = self._validate_config_argument(GE, CODONS_X_INDIVIDUAL, 4, config_parser)
        self._dna_length = self._codon_length * self._num_codons_per_individual
        self._mutation_probability = self._validate_config_argument(GE, MUTATION_PROBABILITY, 0.5, config_parser)
        self._offspring_max_size_factor = self._validate_config_argument(GE, OFFSPRING_FACTOR, 3.5, config_parser)
        self._mating_probability = self._validate_config_argument(GE, MATING_PROBABILITY, 0.9, config_parser)
        self._k_value = self._validate_config_argument(GE, K_VALUE, 3, config_parser)

        #
        # GE configuration methods
        #
        self._selection_type = SelectionType(self._validate_config_argument(GE, SELECTION_TYPE, 0, config_parser))
        self._recombination_type = \
            RecombinationType(self._validate_config_argument(GE, REPLACEMENT_TYPE, 0, config_parser))
        self._replacement_type = ReplacementType(self._validate_config_argument(GE, REPLACEMENT_TYPE, 0, config_parser))
        self._fitness_function_type = \
            FitnessType(self._validate_config_argument(GE, FITNESS_FUNCTION_TYPE, 1, config_parser))

        #
        # BNF Grammar Generation configuration options
        #
        self._features_per_token = self._validate_config_argument(DGG, FEATURES_X_TOKEN, 1, config_parser)
        self._use_boolean_features = self._validate_config_argument(DGG, USE_BOOLEAN_FEATURES, False, config_parser)
        self._use_custom_attributes = self._validate_config_argument(DGG, USE_CUSTOM_ATTRIBUTES, False, config_parser)
        self._use_uniques = self._validate_config_argument(DGG, USE_UNIQUES, True, config_parser)
        self._use_grammar_operators = self._validate_config_argument(DGG, USE_GRAMMAR_OPERATORS, False, config_parser)
        self._use_token_wildcard = self._validate_config_argument(DGG, TOKEN_WILDCARD, False, config_parser)
        self._use_extended_pattern_syntax = \
            self._validate_config_argument(DGG, USE_EXTENDED_PATTERN_SYNTAX, False, config_parser)

        #
        # Configuration validation
        #
        self._check_xps_op_restriction()

        #
        # IO
        #
        self._report_path = \
            self._validate_config_argument('OS', REPORT_PATH, '/tmp/patternOmatic_report.txt', config_parser)

        LOG.debug(f'Configuration parameters: {dict(self)}')

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
        yield 'Selection algorithm', self.selection_type.name
        yield 'Recombination algorithm', self.recombination_type.name
        yield 'Replacement algorithm', self.replacement_type.name
        yield 'Maximum number of features per token', self.features_per_token
        yield 'Using boolean features?', self.use_boolean_features
        yield 'Using custom attributes?', self.use_custom_attributes
        yield 'Using unique feature terminal?', self.use_uniques
        yield 'Using grammar operators?', self.use_grammar_operators
        yield 'Using token wildcards?', self.use_token_wildcard
        yield 'Using extended pattern syntax?', self.use_extended_pattern_syntax
        yield 'Fitness function type', self.fitness_function_type.name
        yield 'Report path', self.report_path

    def _validate_config_argument(self, section, option, default, config_parser):
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
                LOG.error(f'[{section}][{option}] {value}')
            elif isinstance(default, int):
                value = config_parser.getint(section, option, fallback=default)
                LOG.error(f'[{section}][{option}] {value}')
            elif isinstance(default, float):
                value = config_parser.getfloat(section, option, fallback=default)
                LOG.error(f'[{section}][{option}] {value}')
            elif isinstance(default, str):
                value = config_parser.get(section, option, fallback=default)
                LOG.error(f'[{section}][{option}] {value}')
            else:
                value = default
        except ValueError:
            LOG.warning(f'[{section}][{option}] configuration parameter wrongly set. '
                        f'Falling back to its default value: {default}')
            value = default
        return value

    def _preserve_property_type(self, property, value):
        return isinstance(value, type(property))

    @property
    def max_runs(self) -> int:
        return self._max_runs

    @max_runs.setter
    def max_runs(self, value: int) -> None:
        if self._preserve_property_type(self._max_runs, value):
            self._max_runs = value

    @property
    def success_threshold(self) -> float:
        return self._success_threshold

    @success_threshold.setter
    def success_threshold(self, value: float) -> None:
        if self._preserve_property_type(self._success_threshold, value):
            self._success_threshold = value

    @property
    def population_size(self) -> int:
        return self._population_size

    @population_size.setter
    def population_size(self, value: int) -> None:
        if self._preserve_property_type(self._population_size, value):
            self._population_size = value

    @property
    def max_generations(self) -> int:
        return self._max_generations

    @max_generations.setter
    def max_generations(self, value: int) -> None:
        if self._preserve_property_type(self._max_generations, value):
            self._max_generations = value

    @property
    def codon_length(self) -> int:
        return self._codon_length

    @codon_length.setter
    def codon_length(self, value: int) -> None:
        if self._preserve_property_type(self._codon_length, value):
            self._codon_length = value

    @property
    def num_codons_per_individual(self) -> int:
        return self._num_codons_per_individual

    @num_codons_per_individual.setter
    def num_codons_per_individual(self, value: int) -> None:
        if self._preserve_property_type(self._num_codons_per_individual, value):
            self._num_codons_per_individual = value

    @property
    def dna_length(self) -> int:
        return self._dna_length

    @property
    def mutation_probability(self) -> float:
        return self._mutation_probability

    @mutation_probability.setter
    def mutation_probability(self, value: float) -> None:
        if self._preserve_property_type(self._mutation_probability, value):
            self._mutation_probability = value

    @property
    def offspring_max_size_factor(self) -> float:
        return self._offspring_max_size_factor

    @offspring_max_size_factor.setter
    def offspring_max_size_factor(self, value: float) -> None:
        if self._preserve_property_type(self._offspring_max_size_factor, value):
            self._offspring_max_size_factor = value

    @property
    def mating_probability(self) -> float:
        return self._mating_probability

    @mating_probability.setter
    def mating_probability(self, value: float) -> None:
        if self._preserve_property_type(self._mating_probability, value):
            self._mating_probability = value

    @property
    def k_value(self) -> int:
        return self._k_value

    @k_value.setter
    def k_value(self, value: int):
        if self._preserve_property_type(self._k_value, value):
            self._k_value = value

    @property
    def selection_type(self) -> SelectionType:
        return self._selection_type

    @selection_type.setter
    def selection_type(self, value) -> None:
        if self._preserve_property_type(self._selection_type, value):
            self._selection_type = value

    @property
    def recombination_type(self) -> RecombinationType:
        return self._recombination_type

    @recombination_type.setter
    def recombination_type(self, value) -> None:
        if self._preserve_property_type(self._recombination_type, value):
            self._recombination_type = value

    @property
    def replacement_type(self) -> ReplacementType:
        return self._replacement_type

    @replacement_type.setter
    def replacement_type(self, value) -> None:
        if self._preserve_property_type(self._replacement_type, value):
            self._replacement_type = value

    @property
    def features_per_token(self) -> int:
        return self._features_per_token

    @features_per_token.setter
    def features_per_token(self, value: int) -> None:
        if self._preserve_property_type(self._features_per_token, value):
            self._features_per_token = value

    @property
    def use_boolean_features(self) -> bool:
        return self._use_boolean_features

    @use_boolean_features.setter
    def use_boolean_features(self, value: int) -> None:
        if self._preserve_property_type(self._use_boolean_features, value):
            self._use_boolean_features = value

    @property
    def use_custom_attributes(self) -> bool:
        return self._use_custom_attributes

    @use_custom_attributes.setter
    def use_custom_attributes(self, value: int) -> None:
        if self._preserve_property_type(self._use_custom_attributes, value):
            self._use_custom_attributes = value

    @property
    def use_uniques(self) -> bool:
        return self._use_uniques

    @use_uniques.setter
    def use_uniques(self, value: int) -> None:
        if self._preserve_property_type(self._use_uniques, value):
            self._use_uniques = value

    @property
    def use_grammar_operators(self) -> bool:
        return self._use_grammar_operators

    @use_grammar_operators.setter
    def use_grammar_operators(self, value: int) -> None:
        if self._preserve_property_type(self._use_grammar_operators, value):
            self._use_grammar_operators = value
            self._check_xps_op_restriction()

    @property
    def use_token_wildcard(self) -> bool:
        return self._use_token_wildcard

    @use_token_wildcard.setter
    def use_token_wildcard(self, value: bool) -> None:
        if self._preserve_property_type(self._use_token_wildcard, value):
            self._use_token_wildcard = value

    @property
    def use_extended_pattern_syntax(self) -> bool:
        return self._use_extended_pattern_syntax

    @use_extended_pattern_syntax.setter
    def use_extended_pattern_syntax(self, value) -> None:
        if self._preserve_property_type(self._use_extended_pattern_syntax, value):
            self._use_extended_pattern_syntax = value
            self._check_xps_op_restriction()

    @property
    def fitness_function_type(self) -> FitnessType:
        return self._fitness_function_type

    @fitness_function_type.setter
    def fitness_function_type(self, value: int) -> None:
        if self._preserve_property_type(self._fitness_function_type, value):
            self._fitness_function_type = value

    @property
    def report_path(self):
        return self._report_path

    @report_path.setter
    def report_path(self, value: str) -> None:
        if self._preserve_property_type(self._report_path, value):
            self._report_path = value

    #
    # Restrictions
    #
    def _check_xps_op_restriction(self) -> None:
        """
        Spacy's Grammar Operators and Quantifiers and the Spacy's Extended Pattern Syntax can not be used together  at
        the same time in a pattern for the Spacy's Rule Based Matcher.

        This method checks the provided configuration and disables the Spacy's Extended Pattern Syntax if both
        mechanisms are found enabled at the provided configuration.

        Returns: None

        """
        if self._use_extended_pattern_syntax == self._use_grammar_operators is True:
            LOG.warning(f'Extended Pattern Syntax is not compatible with the usage of Grammar Operators. '
                        f'Extended Pattern Syntax has been disabled!')
            self._use_extended_pattern_syntax = False

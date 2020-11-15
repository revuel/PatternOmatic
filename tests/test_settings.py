""" Unit testing module for settings module

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
import configparser
import os
import unittest

from PatternOmatic.settings.config import Config, RecombinationType


class TestConfig(unittest.TestCase):
    """ Test class for settings """

    config = None

    def test_config_is_singleton(self):
        """ Tests config instance is a singleton one """
        another_config = Config()
        super().assertEqual(self.config, another_config)

    def test_config_is_clearable(self):
        """ Tests its possible to renew the singleton instance """
        Config.clear_instance()
        another_config = Config()

        super().assertNotEqual(self.config, another_config)

    def test_config_read_from_path(self):
        """ Tests providing or not providing a configuration file works as expected"""
        # No config file provided
        super().assertEqual(None, self.config.file_path)

        # Correct config file provided

        file_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir), 'config.ini')
        Config.clear_instance()
        self.config = Config(file_path)
        super().assertEqual(file_path, self.config.file_path)

        # Bad path provided
        Config.clear_instance()
        self.config = Config('')
        super().assertEqual(None, self.config.file_path)

    def test_xps_gop_can_not_be_enabled_together(self):
        """ Tests Spacy's Grammar Operators and Extended Patter Syntax can not be enabled both """
        config = Config()
        config.use_grammar_operators = True
        config.use_extended_pattern_syntax = True
        super().assertNotEqual(config.use_grammar_operators, config.use_extended_pattern_syntax)

        config.use_grammar_operators = False
        config.use_extended_pattern_syntax = True
        super().assertEqual(True, config.use_extended_pattern_syntax)

        config.use_grammar_operators = True
        super().assertEqual(False, config.use_extended_pattern_syntax)

    def test_setting_config_attribute_with_wrong_type_has_no_effect(self):
        config = Config()

        config.max_runs = 0.5
        config.use_extended_pattern_syntax = None
        config.fitness_function_type = RecombinationType.RANDOM_ONE_POINT_CROSSOVER
        config.report_path = 0

        super().assertNotEqual(config.max_runs, 0.5)
        super().assertNotEqual(config.use_extended_pattern_syntax, None)
        super().assertNotEqual(config.fitness_function_type, RecombinationType.RANDOM_ONE_POINT_CROSSOVER)
        super().assertNotEqual(config.report_path, 0)

    def test_validate_config_argument(self):
        """ Checks that config arguments are properly fetched according to its type """
        config_parser = configparser.ConfigParser()

        test_section = 'test_section'
        test_option_int = 'test_option_int'
        test_option_float = 'test_option_float'
        test_option_boolean = 'test_option_boolean'
        test_option_string = 'test_option_string'

        config_parser.add_section(test_section)

        config_parser[test_section][test_option_int] = '0'
        config_parser[test_section][test_option_float] = '0.0'
        config_parser[test_section][test_option_boolean] = 'False'
        config_parser[test_section][test_option_string] = ''

        # With valid types
        super().assertEqual(
            0, self.config._validate_config_argument(test_section, test_option_int, 1, config_parser))
        super().assertEqual(
            .0, self.config._validate_config_argument(test_section, test_option_float, .1, config_parser))
        super().assertEqual(
            False, self.config._validate_config_argument(test_section, test_option_boolean, True, config_parser))
        super().assertEqual(
            '', self.config._validate_config_argument(test_section, test_option_string, 'Whatever', config_parser))

        # With wrong type
        config_parser[test_section][test_option_int] = 'False'
        super().assertEqual(
            1, self.config._validate_config_argument(test_section, test_option_int, 1, config_parser))

        # With not even a possible type used by the config parser
        super().assertEqual(
            {}, self.config._validate_config_argument(test_section, test_option_int, {}, config_parser))

    #
    # Helpers
    #
    def setUp(self) -> None:
        """ Fresh Config instance """
        self.config = Config()

    def tearDown(self) -> None:
        """ Destroy Config instance """
        Config.clear_instance()

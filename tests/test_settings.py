""" Unit testing file for settings module """
import unittest

from PatternOmatic.settings.config import Config, RecombinationType


class TestSettings(unittest.TestCase):
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

    #
    # Helpers
    #
    def setUp(self) -> None:
        """ Fresh Config instance """
        self.config = Config()

    def tearDown(self) -> None:
        """ Destroy Config instance """
        Config.clear_instance()

""" Unit testing file for API """
import os
from unittest import TestCase
from PatternOmatic.api import find_patterns
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.log import LOG


class Test(TestCase):

    my_samples = ['Hello world!', 'Goodbye world!']

    def test_find_patterns_when_only_samples_provided(self):
        """ Tests that providing just samples makes the find_pattern keeps working """
        patterns, _ = find_patterns(self.my_samples)
        super().assertEqual(4, len(patterns))

    def test_find_patterns_when_valid_configuration_file_provided(self):
        """ Checks that providing a valid configuration file path loads configuration from that file """

        config_file_path = \
            os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir), 'config.ini')
        _ = find_patterns(self.my_samples, configuration=config_file_path)
        super().assertEqual(config_file_path, Config().file_path)

    def test_find_patterns_when_config_instance_provided(self):
        """ Checks when setting up a Config instance before find_patterns invocation works """
        config = Config()
        config.max_runs = 10
        patterns, _ = find_patterns(self.my_samples)
        super().assertEqual(10, len(patterns))

    def test_find_patterns_when_bad_language_provided(self):
        """ Checks that providing an imaginary language model makes find_patterns use en_core_web_sm """
        with super().assertLogs(LOG) as cm:
            bad_model = 'Something'
            _ = find_patterns(self.my_samples, spacy_language_model_name=bad_model)
            super().assertEqual(f'WARNING:PatternOmatic:Model {bad_model} not found, falling back to '
                                f'patternOmatic\'s default language model: en_core_web_sm', cm.output[1])

    def tearDown(self) -> None:
        """ Destroy Config instance """
        Config.clear_instance()

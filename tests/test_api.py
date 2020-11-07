""" Unit testing file for API """
import os
from unittest import TestCase, skip
from PatternOmatic.api import find_patterns
from PatternOmatic.settings.config import Config


class Test(TestCase):

    my_samples = ['Hello world!', 'Goodbye world!']

    def test_find_patterns_when_only_samples_provided(self):
        """ Tests that providing just samples makes the find_pattern keeps working """
        patterns = find_patterns(self.my_samples)
        super().assertEqual(4, len(patterns))

    def test_find_patterns_when_valid_configuration_file_provided(self):
        """ Checks that providing a valid configuration file path loads configuration from that file """

        config_file_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir),
                                        'config.ini')
        patterns = find_patterns(self.my_samples, configuration=config_file_path)
        super().assertEqual(config_file_path, patterns[0].config.file_path)

    def test_find_patterns_when_config_instance_provided(self):
        """ Checks that providing a Config instance makes find_patterns work with that instance """
        config = Config()
        config.max_runs = 10
        patterns = find_patterns(self.my_samples, configuration=config)
        super().assertEqual(10, len(patterns))

    def test_find_patterns_when_bad_language_provided(self):
        """ Checks that providing an imaginary language model makes find_patterns use en_core_web_sm """
        patterns = find_patterns(self.my_samples, spacy_language_model_name='Something')
        super().assertEqual('en', patterns[0].samples[0].lang_)

    def tearDown(self) -> None:
        """ Destroy Config instance """
        Config.clear_instance()

""" Unit testing file for API module

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
import os
import spacy
from unittest import TestCase, mock
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

    def test_installs_en_core_web_sm_if_not_found(self):
        """ Due to questionable PyPI security policies, check en_core_web_sm installation is fired if not present """
        nlp = spacy.load('en_core_web_sm')

        with mock.patch('PatternOmatic.api.pkg_resources.working_set') as patch_working_set:
            with mock.patch('PatternOmatic.api.spacy_download') as patch_spacy_download:
                with mock.patch('PatternOmatic.api.spacy_load') as patch_spacy_load:
                    patch_working_set.return_value = []
                    patch_spacy_download.return_value = 'I\'ve been fired'
                    patch_spacy_load.return_value = nlp
                    find_patterns(['Hi'])
                    super().assertTrue(patch_spacy_download.called)

    def tearDown(self) -> None:
        """ Destroy Config instance """
        Config.clear_instance()

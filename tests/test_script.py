""" Unit testing file for CLI script module """
import os
import scripts.patternomatic as pom

from unittest import TestCase, mock, skip
from spacy import load as spacy_load
from PatternOmatic.ge.individual import Individual
from PatternOmatic.settings.log import LOG


class TestPatternomaticScript(TestCase):
    """ Test class to verify patternomatic.py correct behaviour """

    nlp = spacy_load('en_core_web_sm')

    samples = [nlp(u'My shirt is white'),
               nlp(u'My cat is black'),
               nlp(u'Your home is comfortable'),
               nlp(u'Their attitude is great')]

    config_file_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir), 'config.ini')

    full_args = ['-s', 'Hello', '-s', 'Goodbye', '-c', config_file_path, '-l', 'en_core_web_sm']

    def test_main(self):
        """ Checks that main method works """
        with super().assertLogs(LOG) as cm:
            pom.main(self.full_args)
            super().assertIn('INFO:PatternOmatic:Best individuals for this execution:', cm.output)

    def test_main_errors_raised(self):
        """ Checks that main raises errors when bad arguments are supplied """
        # No args
        with super().assertRaises(SystemExit):
            pom.main([])

        # Wrong args
        with super().assertRaises(SystemExit):
            pom.main(['-k'])

        # Wrong lang
        with super().assertLogs(LOG) as cm:
            bad_model = 'bad_model'
            args = self.full_args.copy()[:-1]
            args.append(bad_model)
            pom.main(args)
            super().assertEqual(f'WARNING:PatternOmatic:Model {bad_model} not found, falling back to '
                                f'patternOmatic\'s default language model: en_core_web_sm', cm.output[2])

        # Fatal error
        with mock.patch('scripts.patternomatic.ArgumentParser') as mock_arg_parser:
            mock_arg_parser.return_value = Exception('Mocked exception')

            with super().assertRaises(Exception):
                pom.main(self.full_args)

    def test_patternomatic_script(self):
        """ Checks that patternomatic can be run as a script properly """
        script_path = os.path.join(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir), 'scripts', 'patternomatic.py')

        output_signal = os.system('python ' + script_path + ' -s Hello -s Goodbye')
        super().assertEqual(0, output_signal)

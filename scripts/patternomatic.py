#!/usr/bin/python
""" PatternOmatic command line """
import sys
import time
import argparse
import spacy
from spacy.tokens.doc import Doc
from PatternOmatic.ge.stats import Stats
from PatternOmatic.nlp.bnf import dynamic_generator as dgg
from PatternOmatic.ge.population import Population
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.log import LOG


def find_pattern(text_samples: [Doc], config_file_path: str = None) -> None:
    """
    Given some samples, this function finds an optimized pattern to be used by the Spacy's Rule Based Matcher
    Args:
        text_samples: List of Docs (as samples)
        config_file_path: Optional path for configuration file

    Returns: None

    """
    config = Config(config_file_path=config_file_path)
    stats = Stats()
    bnf_g = dgg(text_samples)

    LOG.debug('Starting Execution...')
    for _ in range(0, config.max_runs):
        start = time.monotonic()
        p = Population(text_samples, bnf_g, stats)
        p.evolve()
        end = time.monotonic()
        stats.add_time(end - start)
        stats.calculate_metrics()

    LOG.info(f'Execution report {stats}')
    stats.persist(config.report_path)


if __name__ == '__main__':
    # Execute only if run as a script
    LOG.info('Parsing command line arguments...')
    try:
        cli = argparse.ArgumentParser(description='Finds the Spacy\'s Matcher pattern for the given samples')

        # Samples
        cli.add_argument(
            '-s',
            '--sample',
            action='append',
            required=True,
            nargs='+',
            type=str,
            help='A sample phrase'
        )

        # Spacy Language Model
        cli.add_argument(
            '-l',
            '--language',
            nargs='?',
            type=str,
            default='en_core_web_sm',
            help='Spacy language model to be used'
        )

        # Configuration file to be used
        cli.add_argument(
            '-c',
            '--config',
            nargs='?',
            type=str,
            help='Configuration file path to be used',
            default=None,
        )

        # Parse command line input arguments/options
        parsed_args = cli.parse_args(sys.argv[1:])

        # Set up language model
        try:
            nlp = spacy.load(parsed_args.language)
        except OSError:
            LOG.warning(f'Model {parsed_args.language} not found, '
                        f'falling back to patternOmatic\'s default language model: en_core_web_sm')

            nlp = spacy.load('en_core_web_sm')

        # Convert to Doc sample arguments
        for index, item in enumerate(parsed_args.sample):
            parsed_args.sample[index] = nlp(u' '.join(item))

        #
        # Find pattern
        #
        find_pattern(parsed_args.sample, config_file_path=parsed_args.config)

    except Exception as ex:
        LOG.critical(f'Fatal error: {repr(ex)}')
        raise Exception(ex)

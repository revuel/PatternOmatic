#!/usr/bin/python
""" PatternOmatic command line """
import sys
import argparse
import spacy
import logging
logging.basicConfig(level=logging.DEBUG)
from spacy.tokens.doc import Doc
from PatternOmatic.ge.stats import Stats
from PatternOmatic.nlp.engine import dynagg as dgg
from PatternOmatic.ge.population import Population


def find_pattern(text_samples: [Doc], language_model_path: str = None, configuration_path: str = None):
    """
    Given some samples, this function finds an optimized pattern to be used by the Spacy's Rule Based Matcher
    Args:
        text_samples: Text phrases
        language_model_path: Optional Spacy model language path
        configuration_path: Optional path for configuration file

    Returns: None

    """
    stats = Stats()
    bnf_g = dgg(text_samples)

    p = Population(text_samples, bnf_g, stats)
    p.evolve()

    p2 = Population(text_samples, bnf_g, stats)
    p2.evolve()

    logging.info('Best pattern found: {}'.format(repr(p.best_individual.fenotype)))
    logging.info('Score over sample: {}'.format(p.best_individual.fitness_value))
    logging.info('Measures {}'.format(dict(stats)))


if __name__ == "__main__":
    # execute only if run as a script
    logging.info("Parsing command line arguments...")
    try:
        cli = argparse.ArgumentParser(description='Finds the Spacy\'s Matcher pattern for the given samples')

        # Samples
        cli.add_argument(
            "-s",
            "--sample",
            action='append',
            required=True,
            nargs="+",
            type=str,
            help='A sample phrase'
        )

        # Spacy Language Model
        cli.add_argument(
            "-l",
            "--language",
            nargs="?",
            type=str,
            default="en_core_web_sm",
            help='Spacy language model to be used'
        )

        # Configuration file to be used
        cli.add_argument(
            "-c",
            "--config",
            nargs="?",
            type=str,
            help='Configuration file to be used',
            default=None,
        )

        # Parse command line input arguments/options
        parsed_args = cli.parse_args(sys.argv[1:])

        # Set up language model
        try:
            nlp = spacy.load(parsed_args.language)
        except Exception:
            log.warning('Model {} not found, falling back to patternOmatic\'s default langugage model: '
                        'en_core_web_sm'.format(parsed_args.language))

            nlp = spacy.load('en_core_web_sm')

        # Convert to Doc sample arguments
        for index, item in enumerate(parsed_args.sample):
            parsed_args.sample[index] = nlp(u" ".join(item))

        # Find pattern
        find_pattern(parsed_args.sample)

    except Exception as ex:
        logging.critical(str(ex))
        raise Exception(ex)

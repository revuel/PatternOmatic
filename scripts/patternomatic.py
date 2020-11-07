#!/usr/bin/python
""" PatternOmatic command line """
import sys
from typing import List
from argparse import ArgumentParser
from PatternOmatic.api import find_patterns
from PatternOmatic.settings.log import LOG


def main(args: List) -> None:
    """
    PatternOmatic's script main function wrapper
    Args:
        args: Command Line Input Arguments

    Returns: None

    """
    LOG.info('Parsing command line arguments...')
    try:
        cli = ArgumentParser(
            description='Finds the Spacy\'s Matcher pattern for the given samples',
            epilog='...using actual Artificial Intelligence'
        )

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
        parsed_args = cli.parse_args(args)

        # Convert to Doc sample arguments
        for index, item in enumerate(parsed_args.sample):
            parsed_args.sample[index] = ' '.join(item)

        #
        # Find pattern
        #
        find_patterns(parsed_args.sample,
                      configuration=parsed_args.config,
                      spacy_language_model_name=parsed_args.language)

    except Exception as ex:
        LOG.critical(f'Fatal error: {repr(ex)}')
        raise ex


#
# OS INPUT
#
if __name__ == '__main__': \
    main(sys.argv[1:])

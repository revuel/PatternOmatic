#!/usr/bin/python
""" Command Line Interface module

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

        # Join sample arguments
        for index, item in enumerate(parsed_args.sample):
            parsed_args.sample[index] = ' '.join(item)

        #
        # Find patterns
        #
        patterns_found, _ = find_patterns(
            parsed_args.sample,
            configuration=parsed_args.config,
            spacy_language_model_name=parsed_args.language)

        LOG.info(f'Patterns found: {patterns_found}')

    except Exception as ex:
        LOG.critical(f'Fatal error: {repr(ex)}')
        raise ex


#
# OS INPUT
#
if __name__ == '__main__': \
    main(sys.argv[1:])

""" API module """
import time
from typing import List, Union
from spacy import load as spacy_load

from PatternOmatic.ge.individual import Individual
from PatternOmatic.ge.population import Population
from PatternOmatic.ge.stats import Stats
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.log import LOG
from PatternOmatic.nlp.bnf import dynamic_generator as dgg


def find_patterns(
        samples: List[str],
        configuration: Union[str, Config] = None,
        spacy_language_model_name: str = None) -> List[Individual]:
    """
    Given some samples, this function finds an optimized pattern to be used by the Spacy's Rule Based Matcher
    Args:
        samples: List of Docs (as samples)
        configuration: Configuration to be used, valid inputs:
            - Configuration file path
            - PatternOmatic Config instance
            - None
        spacy_language_model_name: Optional valid Spacy Language Model (Fallbacks to Spacy's en_core_web_sm)

    Returns: None

    """
    LOG.info(f'Loading language model {spacy_language_model_name}...')
    try:
        nlp = spacy_load(spacy_language_model_name)
    except OSError:
        LOG.warning(f'Model {spacy_language_model_name} not found, '
                    f'falling back to patternOmatic\'s default language model: en_core_web_sm')

        nlp = spacy_load('en_core_web_sm')

    LOG.info(f'Building Doc instances...')
    samples = [nlp(sample) for sample in samples]

    if isinstance(configuration, Config.__class__):
        LOG.info(f'Using already existing Config instance: {configuration}')
        config = configuration
    else:
        LOG.info(f'Setting up configuration from the following path: {configuration}...')
        config = Config(config_file_path=configuration)

    stats = Stats()

    bnf_g = dgg(samples)

    LOG.info('Starting Execution...')
    for _ in range(0, config.max_runs):
        start = time.monotonic()
        p = Population(samples, bnf_g, stats)
        p.evolve()
        end = time.monotonic()
        stats.add_time(end - start)
        stats.calculate_metrics()

    LOG.info(f'Execution report {stats}')
    stats.persist()

    LOG.info(f'Best individuals for this execution:')
    stats.most_fitted_accumulator.sort(key=lambda i: i.fitness_value, reverse=True)
    for individual in stats.most_fitted_accumulator:
        LOG.info(f'{individual}')

    return stats.most_fitted_accumulator

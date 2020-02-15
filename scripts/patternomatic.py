""" PatternOmatic wrapper """
import sys
import logging
import spacy
import src.nlp.engine as engine
from src.ge.population import Population
from src.settings.config import Config

config = Config()


def find_pattern(text_samples: str, spacy_language=None, config_path=None):
    """

    Args:
        text_samples: Text phrases
        spacy_language: Optional Spacy model language path
        config_path: Optional path for configuration file

    Returns:

    """
    pass


if __name__ == "__main__":
    # execute only if run as a script
    try:
        find_pattern(sys.argv[0], sys.argv[1], sys.argv[2])
    except Exception as ex:
        logging.critical("Invalid argument list!")
        raise Exception(ex)

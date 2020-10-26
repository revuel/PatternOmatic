# PatternOmatic 0.2.*
Finds patterns matching a given Spacy Docs set

**\#AI · \#EvolutionaryComputation · \#NLP**

[![PatternOmatic logo](https://svgshare.com/i/Qwd.svg)](https://github.com/revuel/PatternOmatic)

[![Built with spaCy](https://img.shields.io/badge/made%20with%20❤%20and-spaCy-09a3d5.svg)](https://spacy.io)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Requirements
- [Python 3.7.3](https://www.python.org/downloads/release/python-373/)
- [Spacy 2.3.*](https://spacy.io/usage/v2-3)

## Basic usage

### From sources
*Clone SCM official repository*

`git clone git@github.com:revuel/PatternOmatic.git`

*Play with Makefile*

- `make venv` to activate proyect's Virtual Environment
- `make reqs` to install dependencies
- `make test` to run Unit Tests
- `make cvrg` to run Code Coverage
- `make build` to build a PyPI package
- `make run` to run PatternOmatic's script with example parameters

### From package
*Install package*

`pip install PatternOmatic`

*Play with the CLI*

```
# Show help 
patternomatic -h

# Example usage
patternomatic -s Hello world -s Goodbye world
```

*Play with the library*
```
""" PatternOmatic library example usage """
import time
import spacy

from PatternOmatic.ge.population import Population
from PatternOmatic.ge.stats import Stats
from PatternOmatic.nlp.bnf import dynamic_generator
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.literals import FitnessType
from PatternOmatic.settings.log import LOG


if __name__ == '__main__':
    # 1) Specify a valid Spacy Language Model (en_core_web_sm already included)
    nlp = spacy.load('en_core_web_sm')

    # 2) Build up some doc samples
    samples = [nlp(u'I am a cat!'),
               nlp(u'You are a dog!'),
               nlp(u'She is a rabbit!')]

    # 3) Set up configuration
    config = Config()
    config.max_runs = 4  # Optional
    config.max_generations = 50  # Optional
    config.fitness_function_type = FitnessType.FULL_MATCH  # Optional

    # 4) Generate BNF
    bnf_grammar = dynamic_generator(samples)

    # 5) Create a Stats instance
    s = Stats()

    # 6) Evolve
    for _ in range(0, config.max_runs):
        start = time.monotonic()
        p = Population(samples=samples, grammar=bnf_grammar, stats=s)
        p.evolve()
        end = time.monotonic()
        s.add_time(end - start)
        s.calculate_metrics()

    # 7) Check results
    LOG.info(f'Best patterns found:')
    for i in s.most_fitted_accumulator:
        LOG.info(f'{i.fenotype}, {i.fitness_value}')
    LOG.info(f'Report: {dict(s)}')

```

---

Author: [Miguel Revuelta](mailto:revuel22@hotmail.com "Contact author"), a humble AI enthusiastic


![<img src="patternomatic_logo.svg" width="100"/>](./patternomatic_logo.svg)

# PatternOmatic 0.2.*
Finds patterns describing a set of a given Spacy Docs

## Requirements
- Python 3.7
- Spacy 2.3

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
    # 1) Specify a valid Spacy language model (en_core_web_sm is already usable)
    nlp = spacy.load('en_core_web_sm')

    # 2) Build up some sample doc samples
    samples = [nlp(u'I am a cat!'),
               nlp(u'You are a dog!'),
               nlp(u'She is a rabbit!')]

    # 3) Set up configuration (optional)
    config = Config()
    config.max_runs = 4
    config.max_generations = 50
    config.fitness_function_type = FitnessType.FULL_MATCH

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
    LOG.info(f'Report {dict(s)}')

```

---

Author: [Miguel Revuelta](mailto:revuel22@hotmail.com "Contact author")

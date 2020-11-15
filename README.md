<img src="https://svgshare.com/i/R3P.svg" width="200" height="200" align="right"/> 

# PatternOmatic 0.2.*

**\#AI · \#EvolutionaryComputation · \#NLP**

[![Built with spaCy](https://img.shields.io/badge/made%20with%20❤%20and-spaCy-09a3d5.svg)](https://spacy.io)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Build Status](https://travis-ci.org/revuel/PatternOmatic.svg?branch=master)](https://travis-ci.org/revuel/PatternOmatic) 
[![Sonar Coverage](https://img.shields.io/sonar/coverage/revuel_PatternOmatic?server=https%3A%2F%2Fsonarcloud.io)](https://sonarcloud.io/dashboard?id=revuel_PatternOmatic)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=revuel_PatternOmatic&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=revuel_PatternOmatic)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=revuel_PatternOmatic&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=revuel_PatternOmatic)
[![GitHub repo size](https://img.shields.io/github/repo-size/revuel/PatternOmatic?color=teal)](#)
[![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/PatternOmatic)](https://libraries.io/pypi/PatternOmatic/sourcerank)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/PatternOmatic?color=FFDF00&label=downloads)](https://pypistats.org/packages/PatternOmatic)
[![PyPI version](https://badge.fury.io/py/PatternOmatic.svg?color=red)](https://badge.fury.io/py/PatternOmatic)

_Discover spaCy's linguistic patterns matching a given set of string samples_

## Requirements
- [Python 3.7.3](https://www.python.org/downloads/release/python-373/)
- [Spacy 2.3.*](https://spacy.io/usage/v2-3)

## Basic usage

### From sources
*[Clone SCM official repository](https://github.com/revuel/PatternOmatic)*

`git clone git@github.com:revuel/PatternOmatic.git`

*Play with Makefile*

- `make venv` to activate project's [Virtual Environment*](https://docs.python.org/3.7/library/venv.html)
- `make libs` to install dependencies
- `make test` to run Unit Tests
- `make coverage` to run Code Coverage
- `make run` to run PatternOmatic's script with example parameters

<sub>* you must have one first</sub>

### From package
*Install package*

`pip install PatternOmatic`

*Play with the CLI*

```
# Show help 
patternomatic.py -h

# Usage example 1: Basic
patternomatic.py -s Hello world -s Goodbye world

# Usage example 2: Using a different language
python -m spacy download es_core_news_sm
patternomatic.py -s Me llamo Miguel -s Se llama PatternOmatic -l es_core_news_sm
```

*Play with the library*
```
""" 
PatternOmatic library client example.
Find linguistic patterns to be used by the spaCy Rule Based Matcher

"""
from PatternOmatic.api import find_patterns, Config

if __name__ == '__main__':

    my_samples = ['I am a cat!', 'You are a dog!', 'She is an owl!']

    # Optionally, let it evolve a little bit more!
    config = Config()
    config.max_generations = 150
    config.max_runs = 3

    patterns_found, _ = find_patterns(my_samples)

    print(f'Patterns found: {patterns_found}')

```
---

## Features

### Generic

&#9989; No OS dependencies, no storage or database required!

&#9989; Lightweight package with just a little direct pip dependencies
- [spaCy](https://pypi.org/project/spacy/2.3.2/)
- [spaCy's en_core_web_sm Language Model](https://github.com/explosion/spacy-models/releases/tag/en_core_web_sm-2.3.0)

&#9989; Easy and highly configurable to boost clever searches

&#9989; Includes basic logging mechanism

&#9989; Includes basic reporting, JSON and CSV format supported. Report file path is configurable

&#9989; Configuration file example provided (config.ini)

&#9989; Default configuration is run if no configuration file provided

&#9989; Provides rollback actions against several possible misconfiguration scenarios

### Evolutionary

&#9989; Basic Evolutionary (Grammatical Evolution) parameters available and configurable

&#9989; Supports two different Evolutionary Fitness functions

&#9989; Supports Binary Tournament Evolutionary Selection Type

&#9989; Supports Random One Point Crossover Evolutionary Recombination Type

&#9989; Supports "µ + λ" Evolutionary Replacement Type

&#9989; Supports "µ ∪ λ" with elitism Evolutionary Replacement Type

&#9989; Supports "µ ∪ λ" without elitism Evolutionary Replacement Type

&#9989; Typical evolutionary performance metrics included:
- Success Rate (SR)
- Mean Best Fitness (MBF)
- Average Evaluations to Solution (AES)

### Linguistic

&#9989; [Compatible with any spaCy Language Model](https://spacy.io/usage/models#languages)

&#9989; [Supports all spaCy's Rule Based Matcher standard Token attributes](https://spacy.io/usage/rule-based-matching#adding-patterns-attributes)

&#9989; [Supports the following spaCy's Rule Based Matcher non standard Token attributes](https://spacy.io/api/token#attributes) [(via underscore)](https://spacy.io/usage/processing-pipelines#custom-components-attributes)
- ent_id
- ent_iob
- ent_kb_id
- has_vector
- is_bracket
- is_currency
- is_left_punct
- is_oov
- is_quote
- is_right_punct
- lang
- norm
- prefix
- sentiment
- string
- suffix
- text_with_ws
- whitespace

&#9989; Supports skipping boolean Token attributes

&#9989; [Supports spaCy's Rule Based Matcher Extended Pattern Syntax](https://spacy.io/usage/rule-based-matching#adding-patterns-attributes-extended)

&#9989; [Supports spaCy's Rule Based Matcher Grammar Operators and Quantifiers](https://spacy.io/usage/rule-based-matching#quantifiers)

&#9989; [Supports Token Wildcard](https://spacy.io/usage/rule-based-matching#adding-patterns-wildcard)

&#9989; Supports defining the number of attributes per token within searched patterns

&#9989; Supports usage of non repeated token attribute values

---

Author: [Miguel Revuelta Espinosa _(revuel)_](mailto:revuel22@hotmail.com "Contact author"), a humble AI enthusiastic

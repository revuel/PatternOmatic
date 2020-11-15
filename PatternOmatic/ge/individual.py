""" Evolutionary Individual related classes module

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
import re
import json

from random import random
from itertools import cycle
from spacy.tokens import Doc
from spacy.matcher import Matcher

from PatternOmatic.ge.stats import Stats
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.log import LOG
from PatternOmatic.settings.literals import FitnessType, S, T, XPS, TOKEN_WILDCARD, UNDERSCORE, P, F, EF, IN, NOT_IN, \
    SLD, SRD, GTH, LTH, GEQ, LEQ, EQQ, XPS_AS


class Fitness(object):
    """ Dispatches the proper fitness type for individual instances """
    __slots__ = ('_fitness', 'config', 'samples', 'fenotype')

    def __init__(self, config, samples, fenotype):
        self.config = config
        self.samples = samples
        self.fenotype = fenotype
        self._dispatch_fitness(self.config.fitness_function_type)

    def __call__(self, *args, **kwargs) -> float:
        return self._fitness()

    def _dispatch_fitness(self, fitness_function_type: FitnessType) -> None:
        """
        Sets the type of the fitness function for an Individual instance
        Args:
            fitness_function_type: The fitness function to be used

        Returns: None

        """
        if fitness_function_type == FitnessType.FULL_MATCH:
            self._fitness = self._fitness_full_match
        else:
            self._fitness = self._fitness_basic

    def _fitness_basic(self) -> float:
        """
        Sets the fitness value for an individual. If makes a partial match over a sample, a score is added
        for that sample even if the matches are only a portion of the sample's length
        Returns: Float (fitness value)

        """
        max_score_per_sample = 1 / len(self.samples)
        matcher = Matcher(self.samples[0].vocab)
        matcher.add(repr(FitnessType.BASIC), None, self.fenotype)
        contact = 0.0

        for sample in self.samples:
            matches = matcher(sample)
            if len(matches) > 0:
                contact += max_score_per_sample

        return self._wildcard_penalty(contact)

    def _fitness_full_match(self) -> float:
        """
        Sets the fitness value for an individual. It only gives a partial score if any of the matches equals the full
        length of the sample
        Returns: Float

        """
        max_score_per_sample = 1 / len(self.samples)

        current_vocab = self.samples[0].vocab

        matcher = Matcher(current_vocab)
        matcher.add(repr(FitnessType.FULL_MATCH), None, self.fenotype)
        contact = 0.0

        for sample in self.samples:
            matches = matcher(sample)
            if len(matches) > 0:
                for match in matches:
                    contact += max_score_per_sample if match[2] == len(sample) and match[1] == 0 else + 0
        return self._wildcard_penalty(contact)

    def _wildcard_penalty(self, contact: float) -> float:
        """
        Applies a penalty for the usage of token wildcard if usage of token wildcard is enabled
        Args:
            contact: Temporary fitness value for the current individual

        Returns: Final fitness value for the current individual

        """
        if self.config.use_token_wildcard:
            num_tokens = len(self.fenotype)
            for item in self.fenotype:
                if item == {}:
                    LOG.debug('Applying token wildcard penalty!')
                    penalty = 1/num_tokens
                    contact -= penalty

        return contact


class Individual(object):
    """ Individual implementation of an AI Grammatical Evolution algorithm in OOP fashion """
    __slots__ = ('config', 'samples', 'grammar', 'stats', 'bin_genotype', 'int_genotype', 'fenotype', 'fitness_value')

    def __init__(self, samples: [Doc], grammar: dict, stats: Stats, dna: str = None):
        """
        Individual constructor, if dna is not supplied, sets up randomly its binary genotype
        Args:
            samples: list of Spacy doc objects
            grammar: Backus Naur Form grammar notation encoded in a dictionary
            stats (Stats): statistics object related with this run
            dna: Optional, binary string representation
        """
        self.config = Config()

        self.samples = samples
        self.grammar = grammar
        self.stats = stats
        self.bin_genotype = self._initialize() if dna is None else self.mutate(dna, self.config.mutation_probability)
        self.int_genotype = self._transcription()
        self.fenotype = self._translation()
        self.fitness_value = Fitness(self.config, self.samples, self.fenotype).__call__()

        # Stats concerns
        self._is_solution()

    @property
    def __dict__(self):
        """ Dictionary representation for a slotted class (that has no dict at all) """
        # Above works just for POPOs
        return {s: getattr(self, s, None) for s in self.__slots__ if s in ('bin_genotype', 'fenotype', 'fitness_value')}

    def __repr__(self):
        """ String representation of a slotted class using hijacked dict """
        return f'{self.__class__.__name__}({self.__dict__})'

    #
    # Problem specific GE methods
    #
    def _initialize(self) -> str:
        """
        Sets up randomly the binary string representation of an individual
        Returns: String, binary fashion

        """
        return ''.join([''.join('1') if random() > 0.5
                        else ''.join('0') for _ in range(0, self.config.dna_length)]).strip()

    def _transcription(self) -> [int]:
        """
        Converts a binary string representation to an integer representation codon by codon
        Returns: List of integers

        """
        return [int(self.bin_genotype[i:(i+self.config.codon_length-1)], 2)
                for i in range(0, len(self.bin_genotype), self.config.codon_length-1)]

    def _translation(self):
        done = False
        symbolic_string = self.grammar[S][0]  # Root
        circular = cycle(self.int_genotype)

        while done is not True:
            # First save previous iteration copy
            old_symbolic_string = symbolic_string
            ci = next(circular)

            for key in self.grammar.keys():
                symbolic_string = self._translate(ci, key, symbolic_string)

            # Check if anything changed from last iteration
            if old_symbolic_string == symbolic_string:
                done = True

        translated_individual = '[' + symbolic_string + ']'

        return json.loads(translated_individual)

    def _translate(self, ci: iter, key, symbolic_string: str):
        """
        Helper method to reduce cognitive overload of the public method with the same name (_translation)
        Args:
            ci: Last circular iterator
            key: Last key in the grammar dict
            symbolic_string: String representation of the individual's Spacy's Rule Based Matcher pattern

        Returns: String representation of the individual's Spacy's Rule Based Matcher pattern

        """
        fire = divmod(ci, len(self.grammar[key]))[1]

        if key in [T, XPS]:
            fired_rule = self.grammar[key][fire]
            if fired_rule == TOKEN_WILDCARD:
                symbolic_string = re.sub(key, "{}", symbolic_string, 1)
            else:
                symbolic_string = re.sub(key, "{" + str(self.grammar[key][fire]) + "}", symbolic_string, 1)

        elif key is UNDERSCORE:
            symbolic_string = re.sub(key, "\"_\"" + ": " + "{" + str(self.grammar[key][fire]) + "}", symbolic_string, 1)

        elif key in [P, T, F, EF]:
            symbolic_string = re.sub(key, str(self.grammar[key][fire]), symbolic_string, 1)

        elif key in [IN, NOT_IN]:
            key_r = key.replace(SLD, '').replace(SRD, '')
            feature = "\"" + key_r + "\"" + ":" + str(self.grammar[key][fire]).replace("\'", "\"").replace("\'", "")
            symbolic_string = re.sub(key, feature, symbolic_string, 1)

        elif key in [GTH, LTH, GEQ, LEQ, EQQ]:
            feature = "\"" + XPS_AS[key] + "\"" + ":" + str(self.grammar[key][fire])
            symbolic_string = re.sub(key, feature, symbolic_string, 1)

        else:
            key_r = key.replace(SLD, '').replace(SRD, '')
            fired_rule = str(self.grammar[key][fire])
            if fired_rule != XPS:
                feature = "\"" + key_r + "\"" + ":" + "\"" + fired_rule + "\""
            else:
                feature = "\"" + key_r + "\"" + ":" + fired_rule
            symbolic_string = re.sub(key, feature, symbolic_string, 1)

        return symbolic_string

    #
    # Generic GA methods
    #
    @classmethod
    def mutate(cls, dna, mutation_probability) -> str:
        """
        Mutates a given dna string by a mutation probability
        Args:
            dna: binary string representation of a dna sequence
            mutation_probability: Chances of each gen to be mutated

        Returns: Binary string

        """
        mutated_dna = ''

        for gen in dna:
            if random() < mutation_probability:
                if gen == '1':
                    mutated_dna += '0'
                else:
                    mutated_dna += '1'
            else:
                mutated_dna += gen
        return mutated_dna

    #
    # Stats concerns
    #
    def _is_solution(self) -> None:
        """
        Method to manage AES for the given RUN

        """
        if self.stats.solution_found is False:
            self.stats.sum_aes(1)
            if self.fitness_value >= self.config.success_threshold:
                LOG.debug('Solution found for this run!')
                self.stats.solution_found = True

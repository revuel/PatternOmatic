""" Individual class """
import re
import json
from random import random
from itertools import cycle
from spacy.tokens import Doc
from spacy.matcher import Matcher
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.literals import *

config = Config()


class Individual(object):
    """
    Individual implementation of a AI Grammatical Evolution algorithm in OOP fashion
    """

    def __init__(self, samples: [Doc], grammar: dict, dna: str = None):
        """
        Individual constructor, if dna is not supplied, sets up randomly its binary genotype
        Args:
            samples: list of Spacy doc objects
            grammar: Backus Naur Form grammar notation encoded in a dictionary
            dna: Optional, binary string representation
        """
        self._samples = samples
        self._grammar = grammar
        self._bin_genotype = self._initialize() if dna is None else self.mutate(dna)
        self._int_genotype = self._transcription()
        self._fenotype = self._translation()
        self._fitness_value = self.fitness()

    ''' Properties & setters '''
    @property
    def samples(self) -> [Doc]:
        return self._samples

    @property
    def grammar(self) -> dict:
        return self._grammar

    @property
    def bin_genotype(self) -> str:
        return self._bin_genotype

    @property
    def int_genotype(self) -> [int]:
        return self._int_genotype

    @property
    def fenotype(self) -> [{}]:
        return self._fenotype

    @property
    def fitness_value(self) -> float:
        return self._fitness_value

    ''' Specific GE methods '''
    @staticmethod
    def _initialize() -> str:
        """
        Sets up randomly the binary string representation of an individual
        Returns: String, binary fashion

        """
        return ''.join([''.join('1') if random() > 0.5 else ''.join('0') for _ in range(0, config.dna_length)]).strip()

    def _transcription(self) -> [int]:
        """
        Converts a binary string representation to an integer representation codon by codon
        Returns: List of integers

        """
        return [int(self.bin_genotype[i:(i+config.codon_length-1)], 2)
                for i in range(0, len(self.bin_genotype), config.codon_length-1)]

    def _translation(self):
        """
        Translates the transcription of the genotype to set an individual fenotype given a grammar.
        Returns: List of dictionaries

        """
        done = False
        symbolic_string = self.grammar[S]
        circular = cycle(self.int_genotype)

        while done is not True:
            # First save previous iteration copy
            old_symbolic_string = symbolic_string
            for key in self.grammar.keys():
                ci = next(circular)
                fire = divmod(ci, len(self.grammar[key]))[1]
                if type(self.grammar[key]) is list:
                    if key in [T, XPS]:
                        symbolic_string = re.sub(key, "{" + str(self.grammar[key][fire]) + "}", symbolic_string, 1)
                    elif key is UNDERSCORE:
                        symbolic_string = re.sub(key, "\"_\"" + ": " + "{" + str(self.grammar[key][fire]) + "}", symbolic_string, 1)
                    elif key in [S, P, T, F, EF]:
                        symbolic_string = re.sub(key, str(self.grammar[key][fire]), symbolic_string, 1)
                    elif key in [IN, NOT_IN]:
                        dkey = key.replace(SLD, '').replace(SRD, '')
                        feature = "\"" + dkey + "\"" + ":" + str(self.grammar[key][fire]).replace("\'", "\"").replace("\'", "")
                        symbolic_string = re.sub(key, feature, symbolic_string, 1)
                    elif key in [GTH, LTH, GEQ, LEQ, EQQ]:
                        feature = "\"" + XPS_AS[key] + "\"" + ":" + str(self.grammar[key][fire])
                        symbolic_string = re.sub(key, feature, symbolic_string, 1)
                    else:
                        dkey = key.replace(SLD, '').replace(SRD, '')
                        fired_rule = str(self.grammar[key][fire])
                        if fired_rule != XPS:
                            feature = "\"" + dkey + "\"" + ":" + "\"" + fired_rule + "\""
                        else:
                            feature = "\"" + dkey + "\"" + ":" + fired_rule
                        symbolic_string = re.sub(key, feature, symbolic_string, 1)
                else:
                    symbolic_string = re.sub(key, str(self.grammar[key]), symbolic_string, 1)

            # Check if anything changed from last iteration
            if old_symbolic_string == symbolic_string:
                done = True

        symbolic_string = re.sub('{{}}', TOKEN_WILDCARD, symbolic_string)
        return json.loads("[" + symbolic_string + "]")

    ''' Generic GA methods '''
    @classmethod
    def mutate(cls, dna) -> str:
        """
        Mutates a given dna string by a mutation probability
        Args:
            dna: binary string representation of a dna sequence

        Returns: Binary string

        """
        mutated_dna = ''

        for gen in dna:
            if random() < config.mutation_probability:
                if gen == '1':
                    mutated_dna += '0'
                else:
                    mutated_dna += '1'
            else:
                mutated_dna += gen
        return mutated_dna

    def fitness(self) -> float:
        """
        A pseudo-factory to different fitness functions
        Returns: Float

        """
        if config.fitness_function_type == FITNESS_BASIC:
            return self._fitness_basic()
        elif config.fitness_function_type == FITNESS_FULLMATCH:
            return self._fitness_fullmatch()
        else:
            raise ValueError('Invalid fitness function type: ', config.fitness_function_type)

    def _fitness_basic(self) -> float:
        """
        Sets the fitness value for an individual.
        Returns: Float (fitness value)

        """
        matchy = Matcher(self.samples[0].vocab)
        matchy.add("basic", None, self.fenotype)
        contact = 0.0
        for sample in self.samples:
            matches = matchy(sample)
            if len(matches) > 0:
                for match in matches:
                    contact += (match[2] - match[1]) / len(sample)
        return contact / len(self.samples) if contact != 0.0 else contact

    def _fitness_fullmatch(self) -> float:
        """
        Sets the fitness value for an individual. It only gives a partial score if any of the matches equals full length
        of the sample
        Returns: Float

        """
        max_score_per_sample = 1 / len(self.samples)

        matchy = Matcher(self.samples[0].vocab)
        matchy.add("basic", None, self.fenotype)
        contact = 0.0

        for sample in self.samples:
            matches = matchy(sample)
            if len(matches) > 0:
                for match in matches:
                    if match[2] == len(sample) and match[1] == 0:
                        contact += max_score_per_sample

        return contact

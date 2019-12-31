""" Individual class """
import re
import json
from random import random
from itertools import cycle
from spacy.tokens import Doc
from spacy.matcher import Matcher
from settings.config import Config
from settings.literals import *

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
        return [int(self._bin_genotype[i:(i+config.codon_length-1)], 2)
                for i in range(0, len(self._bin_genotype), config.codon_length-1)]

    def _translation(self):
        """
        Translates the transcription of the genotype to set an individual fenotype given a grammar.
        Returns: List of dictionaries

        """
        done = False
        symbolic_string = self._grammar[S]
        circular = cycle(self._int_genotype)

        while done is not True:
            # First save previous iteration copy
            old_symbolic_string = symbolic_string
            ci = next(circular)
            for key in self._grammar.keys():
                if type(self._grammar[key]) is list:
                    fire = divmod(ci, len(self._grammar[key]))[1]
                    if key == T:
                        ci = next(circular)
                        fire = divmod(ci, len(self._grammar[key]))[1]
                        symbolic_string = re.sub(key, "{" + str(self._grammar[key][fire]) + "}", symbolic_string, 1)
                    elif key not in [S, P, T, F]:
                        dkey = key.replace(SLD, '').replace(SRD, '')
                        feature = "\"" + dkey + "\"" + ":" + "\"" + str(self._grammar[key][fire]) + "\""
                        symbolic_string = re.sub(key, feature, symbolic_string, 1)
                    else:
                        symbolic_string = re.sub(key, str(self._grammar[key][fire]), symbolic_string, 1)
                else:
                    symbolic_string = re.sub(key, str(self._grammar[key]), symbolic_string, 1)

            # Check if anything changed from last iteration
            if old_symbolic_string == symbolic_string:
                done = True

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
        Sets the fitness value for an individual
        Returns: Float

        """
        if config.fitness_function_type == FITNESS_BASIC:
            matchy = Matcher(self._samples[0].vocab)
            matchy.add("basic", None, self._fenotype)
            contact = 0.0
            for sample in self._samples:
                matches = matchy(sample)
                if len(matches) > 0:
                    for match in matches:
                        contact += (match[2] - match[1]) / len(sample)
            return contact/len(self._samples) if contact != 0.0 else contact
        else:
            raise ValueError('Invalid fitness function type: ', config.fitness_function_type)

    ''' Problem specific methods '''
    def duped_disabling(self):
        """
        Checks at fenotype level if there are duplicated
        Returns:

        """
        # TODO(me): is this method really needed?
        raise NotImplementedError

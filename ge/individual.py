""" Individual class """
import re
import json
from spacy.tokens import Doc
from spacy.matcher import Matcher
from random import random
from itertools import cycle


class Individual(object):
    """ TODO: Docstring """

    def __init__(self, samples: [Doc], grammar: dict, dna: str = None):
        self._samples = samples
        self._grammar = grammar
        self._bin_genotype = self._initialize() if dna is None else self.mutate(dna)
        self._int_genotype = self._transcription()
        self._fenotype = self._decode()
        self._fitness_value = self.fitness()

    ''' Decoding methods '''
    @staticmethod
    def _initialize():
        return ''.join([''.join('1') if random() > 0.5 else ''.join('0') for _ in range(0, 80)]).strip()

    def _transcription(self):
        return [int(self._bin_genotype[i:i+7], 2) for i in range(0, len(self._bin_genotype), 7)]

    def _translation(self):
        pass

    def _decode(self):
        """
            Decodes a given genotype to produce its related fenotype
            :param grammar: Grammar dict
            :param int_list: List of codons integer representation
            :return: String fenotype
            """

        done = False
        symbolic_string = self._grammar["<S>"]
        circular = cycle(self._int_genotype)

        while done is not True:
            old_symbolic_string = symbolic_string  # Check if anything changed from last iteration
            ci = next(circular)
            for key in self._grammar.keys():
                if type(self._grammar[key]) is list:
                    fire = divmod(ci, len(self._grammar[key]))[1]
                    if key == '<T>':
                        ci = next(circular)
                        fire = divmod(ci, len(self._grammar[key]))[1]
                        symbolic_string = re.sub(key, "{" + str(self._grammar[key][fire]) + "}", symbolic_string, 1)
                    elif key not in ['S', '<P>', '<T>', '<F>']:
                        dkey = key.replace('<', '').replace('>', '')
                        feature = "\"" + dkey + "\"" + ":" + "\"" + str(self._grammar[key][fire]) + "\""
                        symbolic_string = re.sub(key, feature, symbolic_string, 1)
                    else:
                        symbolic_string = re.sub(key, str(self._grammar[key][fire]), symbolic_string, 1)
                else:
                    symbolic_string = re.sub(key, str(self._grammar[key]), symbolic_string, 1)

            if old_symbolic_string == symbolic_string:
                done = True

        return json.loads("[" + symbolic_string + "]")

    ''' Evolution methods '''
    @classmethod
    def mutate(cls, dna):

        p_mutation = 0.5
        mutated_dna = ''

        for gen in dna:
            if random() < p_mutation:
                if gen == '1':
                    mutated_dna += '0'
                else:
                    mutated_dna += '1'
            else:
                mutated_dna += gen
        return mutated_dna

    def fitness(self):
        matchy = Matcher(self._samples[0].vocab)
        matchy.add("new", None, self._fenotype)
        contact = 0.0
        for sample in self._samples:  # TODO: check phrase matcher or other alterntives
            matches = matchy(sample)
            if len(matches) > 0:
                for match in matches:
                    contact += (match[2] - match[1]) / len(sample)

        return contact/len(self._samples) if contact != 0.0 else contact

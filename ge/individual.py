""" Individual class """
import re
import json
from spacy.tokens import Doc
from spacy.matcher import Matcher
from random import random
from itertools import cycle


class Individual(object):
    """ TODO: Docstring """

    def __init__(self, samples: [Doc], grammar: dict):
        self._samples = samples
        self._grammar = grammar
        self._bin_genotype = self._initialize()
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

            for key in self._grammar.keys():
                if type(self._grammar[key]) is list:
                    ci = next(circular)
                    fire = divmod(ci, len(self._grammar[key]))[1]
                    if key == '<T>':
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
    def mutate(self):
        pass

    def fitness(self):
        matchy = Matcher(self._samples[0].vocab)
        matchy.add("new", None, self._fenotype)
        contact = 0
        for sample in self._samples:
            if len(matchy(sample)) > 0:
                contact += 1

        return contact/len(self._samples) if contact != 0 else 0.0

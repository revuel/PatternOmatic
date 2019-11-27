""" Individual class """
import re
import json
from random import randint
from itertools import cycle


class Individual(object):
    """ TODO: Docstring """

    def __init__(self, grammar: dict):
        self._grammar = grammar
        self._bin_genotype = None
        self._int_genotype = [randint(0, 255) for i in range(1,10)]
        self._fenotype = self.decode()
        self._fitness_value = None

    ''' Decoding methods '''
    def transcription(self):
        pass

    def translation(self):
        pass

    def decode(self):
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
        pass

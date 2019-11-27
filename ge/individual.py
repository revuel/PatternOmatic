""" Individual class """
import re
import json
from itertools import cycle


class Individual(object):
    """ TODO: Docstring """

    def __init__(self):
        self._bin_genotype = None
        self._int_genotype = None
        self._fenotype = None
        self._fitness_value = None

    ''' Decoding methods '''
    def transcription(self):
        pass

    def translation(self):
        pass

    def decode(self, grammar: dict):
        """
            Decodes a given genotype to produce its related fenotype
            :param grammar: Grammar dict
            :param int_list: List of codons integer representation
            :return: String fenotype
            """

        done = False
        symbolic_string = grammar["<S>"]
        circular = cycle(self._int_genotype)

        while done is not True:
            old_symbolic_string = symbolic_string  # Check if anything changed from last iteration

            for key in grammar.keys():
                if type(grammar[key]) is list:
                    ci = next(circular)
                    fire = divmod(ci, len(grammar[key]))[1]
                    if key == '<T>':
                        symbolic_string = re.sub(key, "{" + str(grammar[key][fire]) + "}", symbolic_string, 1)
                    elif key not in ['S', '<P>', '<T>', '<F>']:
                        dkey = key.replace('<', '').replace('>', '')
                        feature = "\"" + dkey + "\"" + ":" + "\"" + str(grammar[key][fire]) + "\""
                        symbolic_string = re.sub(key, feature, symbolic_string, 1)
                    else:
                        symbolic_string = re.sub(key, str(grammar[key][fire]), symbolic_string, 1)
                else:
                    symbolic_string = re.sub(key, str(grammar[key]), symbolic_string, 1)

            if old_symbolic_string == symbolic_string:
                done = True

        return json.loads("[" + symbolic_string + "]")

    ''' Evolution methods '''
    def mutate(self):
        pass

    def fitness(self):
        pass

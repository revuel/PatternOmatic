""" Population class """
from spacy.tokens import Doc


class Population(object):
    """ TODO: Docstring """

    def __init__(self, samples: [Doc]):
        self.generation = list()
        self.offspring = list()

    def sort(self):
        pass

    def selection(self):
        pass

    def recombination(self):
        pass

    def replacement(self):
        pass

    def evolve(self):
        pass

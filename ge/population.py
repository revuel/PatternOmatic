""" Population class """
from spacy.tokens import Doc
from spacy.matcher import Matcher
from ge.individual import Individual


class Population(object):
    """ TODO: Docstring """

    def __init__(self, samples: [Doc], grammar: dict, size: int):
        self._samples = samples
        self._grammar = grammar
        self._generation = self._initialize(grammar, size)
        self._offspring = list()
        self._max_generations = 100

    def _initialize(self, grammar: dict, size: int) -> [Individual]:
        """ Initializes the first generation  """
        return [Individual(self._samples, self._grammar) for _ in range(0, size)]

    def sort(self):
        """ Sorts individual lists by fitness """
        pass

    def _selection(self):
        """ Selects members of the current generation into the mating pool in order to produce offspring """
        pass

    def _recombination(self):
        """ Creates the offspring recombining the mating pool """
        pass

    def _replacement(self):
        """ Produces the new generation """
        pass

    def evolve(self):
        """ Search Engine """
        for _ in range(self._max_generations):
            self._selection()
            self._recombination()
            self._replacement()

""" Entry Point """
import spacy
import nlp.engine as engine
import ge.individual
from ge.population import Population

''' Engine '''
nlp = spacy.load("en_core_web_sm")

from spacy.matcher import Matcher

# Receive samples
sample_list = [nlp(u'Fuck it!'),
               nlp(u'Fuck off!'),
               nlp(u'Fuck all!'),
               nlp(u'Fuck you!')]

grammar = engine.dynagg(sample_list)


for k in grammar.keys():
    print(k, ":", str(grammar[k]))

''' GE '''

population = Population(sample_list, grammar, 10)

for i in population._generation:
    print(str(i._fenotype), ':', str(i._fitness_value))

population._generation[0].fitness()
population.evolve()

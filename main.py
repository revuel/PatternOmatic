""" Entry Point """
import spacy
import nlp.engine as engine
import ge.individual
from ge.population import Population

''' Engine '''
nlp = spacy.load("en_core_web_sm")

from spacy.matcher import Matcher

# Receive samples
sample_list = [nlp.tokenizer(u'Fuck it!'),
               nlp.tokenizer(u'Fuck off!'),
               nlp.tokenizer(u'Fuck all!'),
               nlp.tokenizer(u'Fuck you!')]

grammar = engine.dynagg(sample_list)

sample_list = [nlp(u'Fuck it!'),
               nlp(u'Fuck off!'),
               nlp(u'Fuck all!'),
               nlp(u'Fuck you!')]

for k in grammar.keys():
    print(k, ":", str(grammar[k]))

''' GE '''

population = Population(sample_list, grammar, 20)
population._info()
population.evolve()


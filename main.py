""" Entry Point """
import spacy
import nlp.engine as engine
from ge.population import Population

''' Engine '''
nlp = spacy.load("en_core_web_sm")

from spacy.matcher import Matcher

# Receive samples
sample_list = [nlp.tokenizer(u'Fuck it!'),
               nlp.tokenizer(u'Fuck off!'),
               nlp.tokenizer(u'Fuck all!'),
               nlp.tokenizer(u'Fuck you!'),
               nlp.tokenizer(u'Fuck you all!'),
               nlp.tokenizer(u'Fuck!')]

grammar = engine.dynagg(sample_list)

sample_list = [nlp(u'Fuck it!'),
               nlp(u'Fuck off!'),
               nlp(u'Fuck all!'),
               nlp(u'Fuck you!'),
               nlp(u'Fuck you all!'),
               nlp(u'Fuck!')]

for k in grammar.keys():
    print(k, ":", str(grammar[k]))

''' GE '''

population = Population(sample_list, grammar, 20)
population.evolve()

print(str(population._generation[0]._fenotype))
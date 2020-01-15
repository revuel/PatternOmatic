""" Entry Point """
import spacy
import nlp.engine as engine
from ge.population import Population

''' Engine '''
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(nlp.create_pipe("sentencizer"), first=True)

# Receive samples
sample_list = [nlp(u'Fuck it!'),
               nlp(u'Fuck off!'),
               nlp(u'Fuck all!'),
               nlp(u'Fuck you!'),
               nlp(u'Fuck you all!'),
               nlp(u'Fuck!')]

grammar = engine.dynagg(sample_list)

for k in grammar.keys():
    print(k, ":", str(grammar[k]))

''' GE '''
population = Population(sample_list, grammar)
population.evolve()

print("Fenotype:", str(population._best_individual._fenotype), "Fitness:", population._best_individual._fitness_value)

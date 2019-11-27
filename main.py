""" Entry Point """
import spacy
import nlp.engine as engine
import ge.individual as indi
import ge.population as pop

''' Engine '''
nlp = spacy.load("en_core_web_sm")

# Receive samples
sample_list = [nlp.tokenizer(u'Fuck it!'),
               nlp.tokenizer(u'Fuck off!'),
               nlp.tokenizer(u'Fuck all!'),
               nlp.tokenizer(u'Fuck you!')]

grammar = engine.dynagg(sample_list)


for k in grammar.keys():
    print(k, ":", str(grammar[k]))

''' GE '''

dude_1 = indi.Individual(grammar)
dude_2 = indi.Individual(grammar)
dude_3 = indi.Individual(grammar)
dude_4 = indi.Individual(grammar)

print(str(dude_1._decode()))
print(str(dude_2._decode()))
print(str(dude_3._decode()))
print(str(dude_4._decode()))



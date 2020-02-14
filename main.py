""" Entry Point """


if __name__ == "__main__":

    import spacy
    import nlp.engine as engine
    from ge.population import Population
    from settings.config import Config
    from settings.literals import *

    ''' Engine '''
    nlp = spacy.load("en_core_web_sm")
    # nlp.add_pipe(nlp.create_pipe("sentencizer"), before="parser")

    print(str(nlp.pipe_names))

    config = Config()

    config.mutation_probability = 0.0
    config.fitness_function_type = FITNESS_FULLMATCH

    # Samples list
    sample_list = [nlp(u'I am a raccoon!'),
               nlp(u'You are a cat!'),
               nlp(u'Is she a rabbit?'),
               nlp(u'This is a test')]

    # Build BFN grammar
    grammar = engine.dynagg(sample_list)

    for k in grammar.keys():
        print(k, ":", str(grammar[k]))

    ''' GE '''
    # Init
    population = Population(sample_list, grammar)

    # Search
    population.evolve()

    print("Fenotype:", str(population.best_individual.fenotype), "Fitness:",
          population.best_individual.fitness_value,
          str(population.best_individual.bin_genotype))

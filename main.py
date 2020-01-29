""" Entry Point """


if __name__ == "__main__":

    import spacy
    import nlp.engine as engine
    from ge.population import Population

    ''' Engine '''
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe(nlp.create_pipe("sentencizer"), before="parser")

    print(str(nlp.pipe_names))

    # Receive samples
    sample_list = [nlp(u'Fuck it!'),
                   nlp(u'Fuck off!'),
                   nlp(u'Fuck all!'),
                   nlp(u'Fuck you!'),
                   nlp(u'Fuck you all!'),
                   nlp(u'Fuck!')]

    # Build BFN grammar
    grammar = engine.dynagg(sample_list)

    for k in grammar.keys():
        print(k, ":", str(grammar[k]))

    ''' GE '''
    # Init
    population = Population(sample_list, grammar)

    # Search
    population.evolve()

    print("Fenotype:", str(population.best_individual.fenotype), "Fitness:", population.best_individual.fitness_value)

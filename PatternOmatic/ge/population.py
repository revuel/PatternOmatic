""" Population class """
import random
from spacy.tokens import Doc
from PatternOmatic.ge.individual import Individual
from PatternOmatic.ge.stats import Stats
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.literals import *
from PatternOmatic.settings.log import LOG


class Population(object):
    """ Population implementation of an AI Grammatical Evolution algorithm in OOP fashion """

    def __init__(self, samples: [Doc], grammar: dict, stats: Stats):
        """
        Population constructor, initializes a list of Individual objects
        Args:
            samples: list of Spacy doc objets
            grammar: Backus Naur Form grammar notation encoded in a dictionary
        """
        self._config = Config()

        self._samples = samples
        self._grammar = grammar
        self._stats = stats
        self._generation = self._birth()
        self._offspring = list()
        self._best_individual = None

    #
    # Properties & setters
    #
    @property
    def config(self) -> Config:
        return self._config

    @property
    def samples(self) -> [Doc]:
        return self._samples

    @property
    def grammar(self) -> dict:
        return self._grammar

    @property
    def stats(self):
        return self._stats

    @property
    def generation(self) -> [Individual]:
        return self._generation

    @generation.setter
    def generation(self, generation: [Individual]):
        self._generation = generation

    @property
    def offspring(self) -> [Individual]:
        return self._offspring

    @offspring.setter
    def offspring(self, offspring: [Individual]):
        self._offspring = offspring

    @property
    def best_individual(self) -> Individual:
        return self._best_individual

    @best_individual.setter
    def best_individual(self, best_individual: Individual):
        self._best_individual = best_individual

    def _birth(self) -> [Individual]:
        """
        Initializes the first generation
        Returns: A list of individual objects

        """
        return [Individual(self.samples, self.grammar, self.stats) for _ in range(0, self.config.dna_length)]

    def _best_challenge(self):
        """
        Compares current generation best fitness individual against previous generation best fitness individual.
        Updates the best individual attribute accordingly
        """
        if self.best_individual is not None:
            if self.generation[0].fitness_value > self.best_individual.fitness_value:
                self.best_individual = self.generation[0]
        else:
            self.best_individual = self.generation[0]

    #
    # Evolutionary operators dispatcher
    #
    def _selection(self) -> [Individual]:
        """
        Selects members of the current generation into the mating pool in order to produce offspring
        Returns: a list of individuals

        """
        LOG.debug('Selecting members...')
        if self.config.selection_type == BINARY_TOURNAMENT:
            return self._binary_tournament()
        elif self.config.selection_type == K_TOURNAMENT:
            return self._k_tournament()
        else:
            raise ValueError('Invalid selection type: ', self.config.selection_type)

    def _recombination(self, mating_pool: [Individual]):
        """
        A pseudo-factory to different recombination types
        Args:
            mating_pool: A list of individuals selected from the current generation

        Returns: A list of new individuals, offspring of the current generation

        """
        LOG.debug('Spawning offspring...')
        if self.config.recombination_type == RANDOM_ONE_POINT_CROSSOVER:
            return self._random_one_point_crossover(mating_pool)
        else:
            raise ValueError('Invalid recombination type: ', self.config.recombination_type)

    def _replacement(self) -> None:
        """
        A pseudo-factory to different recombination types

        """
        LOG.debug('Replacing...')
        if self.config.replacement_type == MU_PLUS_LAMBDA:
            return self._mu_plus_lambda()
        elif self.config.replacement_type == MU_LAMBDA_WITH_ELITISM:
            return self._mu_lambda_elite()
        elif self.config.replacement_type == MU_LAMBDA_WITHOUT_ELITISM:
            return self._mu_lambda_no_elite()
        else:
            raise ValueError('Invalid replacement type: ', self.config.replacement_type)

    #
    # Evolutionary operator implementations
    #
    def _binary_tournament(self):
        """
        Selection type: Selects members of the current generation into the mating pool in order to produce offspring
        Returns:

        """
        mating_pool = []

        while len(mating_pool) <= len(self.generation):
            i = random.randint(0, len(self.generation) - 1)
            j = i

            while j == i:
                j = random.randint(0, len(self.generation) - 1)

            i = self.generation[i]
            j = self.generation[j]

            if i.fitness_value >= j.fitness_value:
                mating_pool.append(i)
            else:
                mating_pool.append(j)

        return mating_pool

    def _k_tournament(self):
        """
        Selection type: Selects members of the current generation into the mating pool in order to produce offspring
        Returns:

        """
        # TODO(me): k tournament
        raise NotImplementedError

    def _random_one_point_crossover(self, mating_pool: [Individual]) -> [Individual]:
        """
        Recombination type: Creates the offspring recombining the mating pool
        Args:
            mating_pool: A list of individuals selected from the current generation

        Returns: A list of new individuals, offspring of the current generation

        """
        offspring = []
        offspring_max_size = round(len(self.generation) * self.config.offspring_max_size_factor)

        while len(offspring) <= offspring_max_size:
            parent_1 = random.choice(mating_pool)
            parent_2 = random.choice(mating_pool)

            if random.random() < self.config.mating_probability:
                cut = random.randint(1, self.config.codon_length - 1) * self.config.num_codons_per_individual

                # Create children
                child_1 = \
                    Individual(self.samples, self.grammar, self.stats,
                               dna=parent_1.bin_genotype[:cut] + parent_2.bin_genotype[
                                                                 -(self.config.dna_length - cut):])

                child_2 = \
                    Individual(self.samples, self.grammar, self.stats,
                               dna=parent_2.bin_genotype[:cut] + parent_1.bin_genotype[
                                                                 -(self.config.dna_length - cut):])

                offspring.append(child_1)
                offspring.append(child_2)

        return offspring

    def _mu_plus_lambda(self):
        """
        Replacement type: Produces the new generation and cleans up the offspring pool

        """
        replacement_pool = self.generation + self.offspring
        replacement_pool.sort(key=lambda i: i.fitness_value, reverse=True)
        self.generation = replacement_pool[:len(self.generation)]
        self.offspring = []

    def _mu_lambda_elite(self):
        """
        Replacement type: Produces the new generation and cleans up the offspring pool

        """
        self.generation.sort(key=lambda i: i.fitness_value, reverse=True)
        self.offspring.sort(key=lambda i: i.fitness_value, reverse=True)
        self.generation[1:len(self.generation)] = self.offspring[0:len(self.generation)]
        self.offspring = []

    def _mu_lambda_no_elite(self):
        """
        Replacement type: Produces the new generation and cleans up the offspring pool

        """
        self.offspring.sort(key=lambda i: i.fitness_value, reverse=True)
        self.generation = self.offspring[0:len(self.generation)]
        self.offspring = []

    #
    # Evolution
    #
    def evolve(self):
        """ Search Engine
        1) Selects individuals of the current generation to constitute who will mate
        2) Crossover or recombination of the previously selected individuals
        3) Replace/mix the this generation with the offspring
        4) Save the best individual by fitness
        5) Calculates statistics for this Run """

        LOG.info('Evolution taking place!')

        self.stats.reset()

        for _ in range(self.config.max_generations):
            mating_pool = self._selection()
            self.offspring = self._recombination(mating_pool)
            self._replacement()
            self._best_challenge()

        LOG.info(f'Best candidate found on this run: {dict(self.best_individual)}')

        # Stats concerns
        self.stats.add_most_fitted(self.best_individual)
        self.stats.add_mbf(self.best_individual.fitness_value)

        if self.best_individual.fitness_value > self.config.success_threshold:
            self.stats.add_sr(True)
        else:
            self.stats.add_sr(False)

        self.stats.calculate_metrics()

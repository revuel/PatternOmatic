""" GE Various metrics are saved here """
import operator


class Stats(object):
    """ Class responsible of handling performance metrics """
    def __init__(self):
        """ Stats instances constructor"""
        self._success_rate_accumulator = list()
        self._mbf_accumulator = list()
        self._aes_accumulator = list()
        self._time_accumulator = list()
        self._most_fitted_accumulator = list()
        self._solution_found = False
        self._success_rate = None
        self._mbf = None
        self._aes = None
        self._mean_time = None

        self._aes_counter = 0

    def __iter__(self):
        yield 'SR', self._success_rate
        yield 'MBF', self._mbf
        yield 'AES', self._aes
        yield 'Mean Time', self._mean_time
        yield 'Best Individual', dict(self.get_most_fitted())

    #
    # Accumulators & Counters
    #
    def add_sr(self, sr: bool) -> None:
        """
        Adds a new Success Rate value to the accumulator
        Args:
            sr: Boolean value that indicates if the RUN succeeded (True) or not (False)

        """
        self._success_rate_accumulator.append(sr)

    def add_mbf(self, bf: float) -> None:
        """
        Adds a new Best Fitness value to the accumulator
        Args:
            bf: Best fitness fount over a RUN

        """
        self._mbf_accumulator.append(bf)

    def add_aes(self, es: int) -> None:
        """
        Adds a new Evaluations to Solution value to the accumulator
        Args:
            es: Number of evaluations to solution over a RUN

        """
        self._aes_accumulator.append(es)

    def add_time(self, time: float) -> None:
        """
        Adds a new Time lapsed value to the accumulator
        Args:
            time: Time lapsed of a RUN

        """
        self._time_accumulator.append(time)

    def add_most_fitted(self, indi: any) -> None:
        """
        Adds a new individual to the accumulator
        Args:
            indi: Individual with best fitness found over a RUN

        Returns:

        """
        self._most_fitted_accumulator.append(indi)

    def sum_aes(self, es: int) -> None:
        """
        Sums a new Evaluations to Solution value to the counter
        Args:
            es: Evalutations to Solution of a given Run

        Returns:

        """
        self._aes_counter += es

    #
    # Metrics
    #
    def reset(self):
        """ Resets variables that depend on the run """
        self._aes_counter = 0
        self._solution_found = False

    def calculate_metrics(self):
        """ Calculates the common GE evaluation metrics """
        self.add_aes(self._aes_counter)
        self._success_rate = Stats.avg(self._success_rate_accumulator)
        self._mbf = Stats.avg(self._mbf_accumulator)
        self._aes = Stats.avg(self._aes_accumulator)
        self._mean_time = Stats.avg(self._time_accumulator)

    @property
    def success_rate(self) -> float:
        """
        Average of the RUNS that succeeded
        Returns: SR value for this Execution

        """
        return self._success_rate

    @property
    def mbf(self) -> float:
        """
        Mean Best Fitness
        Returns: MBF of this Execution

        """
        return self._mbf

    @property
    def aes(self) -> float:
        """
        Average Evaluations to Solution
        Returns: AES of this Execution

        """
        return self._aes

    @property
    def mean_time(self) -> float:
        """
        Time lapsed for this Execution
        Returns: Mean time of this Execution

        """
        return self._mean_time

    @property
    def solution_found(self) -> bool:
        return self._solution_found

    @solution_found.setter
    def solution_found(self, value: bool):
        self._solution_found = value

    #
    # Auxiliary methods
    #
    def get_most_fitted(self):
        """
        Best individual found
        Returns: Individual with Best Fitness found for this Execution

        """
        return max(self._most_fitted_accumulator, key=operator.attrgetter('fitness_value'))

    @staticmethod
    def avg(al: list) -> float:
        return sum(al) / len(al) if len(al) > 0 else 0.0

    @staticmethod
    def persist(stats: any):
        pass

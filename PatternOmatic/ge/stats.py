""" GE Various metrics are saved here """
import operator
from PatternOmatic.settings.log import LOG


class Stats(object):
    """ Class responsible of handling performance metrics """
    __slots__ = [
        'success_rate_accumulator',
        'mbf_accumulator',
        'aes_accumulator',
        'time_accumulator',
        'most_fitted_accumulator',
        'solution_found',
        'success_rate',
        'mbf',
        'aes',
        'mean_time',
        'aes_counter'
    ]

    def __init__(self):
        """ Stats instances constructor """
        self.success_rate_accumulator = list()
        self.mbf_accumulator = list()
        self.aes_accumulator = list()
        self.time_accumulator = list()
        self.most_fitted_accumulator = list()
        self.solution_found = False
        self.success_rate = None
        self.mbf = None
        self.aes = None
        self.mean_time = None

        self.aes_counter = 0

    def __iter__(self):
        """ Iterable instance """
        yield 'SR', self.success_rate
        yield 'MBF', self.mbf
        yield 'AES', self.aes
        yield 'Mean Time', self.mean_time
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
        self.success_rate_accumulator.append(sr)

    def add_mbf(self, bf: float) -> None:
        """
        Adds a new Best Fitness value to the accumulator
        Args:
            bf: Best fitness fount over a RUN

        """
        self.mbf_accumulator.append(bf)

    def add_aes(self, es: int) -> None:
        """
        Adds a new Evaluations to Solution value to the accumulator
        Args:
            es: Number of evaluations to solution over a RUN

        """
        self.aes_accumulator.append(es)

    def add_time(self, time: float) -> None:
        """
        Adds a new Time lapsed value to the accumulator
        Args:
            time: Time lapsed of a RUN

        """
        self.time_accumulator.append(time)

    def add_most_fitted(self, indi: any) -> None:
        """
        Adds a new individual to the accumulator
        Args:
            indi: Individual with best fitness found over a RUN

        Returns:

        """
        self.most_fitted_accumulator.append(indi)

    def sum_aes(self, es: int) -> None:
        """
        Sums a new Evaluations to Solution value to the counter
        Args:
            es: Evalutations to Solution of a given Run

        Returns:

        """
        self.aes_counter += es

    #
    # Metrics
    #
    def reset(self):
        """ Resets variables that depend on the run """
        self.aes_counter = 0
        self.solution_found = False

    def calculate_metrics(self):
        """ Calculates the common GE evaluation metrics """
        self.add_aes(self.aes_counter)
        self.success_rate = Stats.avg(self.success_rate_accumulator)
        self.mbf = Stats.avg(self.mbf_accumulator)
        self.aes = Stats.avg(self.aes_accumulator)
        self.mean_time = Stats.avg(self.time_accumulator)

    #
    # Auxiliary methods
    #
    def get_most_fitted(self):
        """
        Best individual found
        Returns: Individual with Best Fitness found for this Execution

        """
        return max(self.most_fitted_accumulator, key=operator.attrgetter('fitness_value'))

    @staticmethod
    def avg(al: list) -> float:
        """
        Returns the mean of a list if the list is not empty
        Args:
            al: List instance

        Returns: float, the mean/average of the list

        """
        return sum(al) / len(al) if len(al) > 0 else 0.0

    def persist(self, report_path: str, report_format: str = 'csv') -> None:
        """
        Makes or append execution result to file
        Args:
            report_path: Full Os path and filename for the report
            report_format: Append stats as json or csv without headers

        Returns: None

        """
        if report_format == 'json':
            with open(report_path, mode='a+') as f:
                f.writelines(str(dict(self)) + '\n')
        elif report_format == 'csv':
            with open(report_path, mode='a+') as f:
                f.writelines(self._to_csv() + '\n')
        else:
            LOG.warning(f'Unexpected format {format}, falling back to default format (csv)')
            with open(report_path, mode='a+') as f:
                f.writelines(self._to_csv() + '\n')

    def _to_csv(self):
        """
        Generates Comma Separated Value (csv) representation of a Stats instance object
        Returns: String, csv instance representation

        """
        csv = ''
        for k, v in dict(self).items():
            if not type(v) is dict:
                csv = csv + str(v) + '\t'
            else:
                # Fenotype json representation requires adjustment
                csv = csv + str(v['Fitness']) + '\t' + str(v['Fenotype']).replace(', ', '|')
        return csv

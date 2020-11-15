""" Grammatical Evolution performance metrics module

This file is part of PatternOmatic.

Copyright © 2020  Miguel Revuelta Espinosa

PatternOmatic is free software: you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License
as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

PatternOmatic is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with PatternOmatic. If not, see <https://www.gnu.org/licenses/>.

"""
import operator
from time import time

from PatternOmatic.settings.literals import ReportFormat
from PatternOmatic.settings.config import Config


class Stats(object):
    """ Class responsible of handling performance metrics """
    __slots__ = [
        'config',
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
        self.config = Config()
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

    @property
    def __dict__(self):
        """ Dictionary representation for a slotted class (that has no dict at all) """
        # Above works just for POPOs
        stats_dict = \
            {s: getattr(self, s, None) for s in self.__slots__ if s in ('success_rate', 'mbf', 'aes', 'mean_time')}

        most_fitted = self.get_most_fitted()
        most_fitted_dict = {'most_fitted': most_fitted.__dict__} if most_fitted is not None else {'most_fitted': None}
        stats_dict.update(most_fitted_dict)

        return stats_dict

    def __repr__(self):
        """ String representation of a slotted class using hijacked dict """
        return f'{self.__class__.__name__}({self.__dict__})'

    def __iter__(self):
        """ Enable dict(self) """
        yield from self.__dict__.items()

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

    def add_time(self, time_interval: float) -> None:
        """
        Adds a new Time lapsed value to the accumulator
        Args:
            time_interval: Time lapsed of a RUN

        """
        self.time_accumulator.append(time_interval)

    def add_most_fitted(self, individual: any) -> None:
        """
        Adds a new individual to the accumulator
        Args:
            individual: Individual with best fitness found over a RUN

        Returns:

        """
        self.most_fitted_accumulator.append(individual)

    def sum_aes(self, es: int) -> None:
        """
        Sums a new Evaluations to Solution value to the counter
        Args:
            es: Number of evaluations to Solution of a given Run

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
        return max(self.most_fitted_accumulator, key=operator.attrgetter('fitness_value')) \
            if len(self.most_fitted_accumulator) > 0 else None

    @staticmethod
    def avg(al: list) -> float:
        """
        Returns the mean of a list if the list is not empty
        Args:
            al: List instance

        Returns: float, the mean/average of the list

        """
        return sum(al) / len(al) if len(al) > 0 else 0.0

    def persist(self) -> None:
        """
        Makes or append execution result to file. If no valid format is specified CSV will be used as default
        Returns: None

        """
        if self.config.report_format == ReportFormat.JSON:
            with open(self.config.report_path, mode='a+') as f:
                f.writelines(f'{dict(self)}' + '\n')
        else:
            with open(self.config.report_path, mode='a+') as f:
                f.writelines(self._to_csv() + '\n')

    def _to_csv(self):
        """
        Generates Comma Separated Value (csv) representation of a Stats instance object
        Returns: String, csv instance representation

        """
        csv = f'{time()}' + '\t'

        for k, v in self.__dict__.items():
            if not type(v) is dict:
                csv = csv + str(v) + '\t'
            else:
                for _, vi in v.items():
                    csv = csv + str(vi) + '\t'
        return csv

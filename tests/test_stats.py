""" Unit testing module for stats module

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
import os
from unittest import TestCase, mock

from PatternOmatic.ge.individual import Individual
from PatternOmatic.ge.stats import Stats
from PatternOmatic.settings.config import Config
from PatternOmatic.settings.literals import ReportFormat


class TestStats(TestCase):
    """ Tests for Stats class """

    stats = None
    test_report_path_file = 'test_report_path_file.txt'
    fitness_value_literal = 'fitness_value'

    def test_add_sr(self):
        """ SR accumulator works """
        self.stats.add_sr(True)
        super().assertListEqual([True], self.stats.success_rate_accumulator)

    def test_add_mbf(self):
        """ MBF accumulator works """
        self.stats.add_mbf(0.5)
        super().assertListEqual([0.5], self.stats.mbf_accumulator)

    def test_add_aes(self):
        """ AES accumulator works """
        self.stats.add_aes(10)
        super().assertListEqual([10], self.stats.aes_accumulator)

    def test_add_time(self):
        """ Time accumulator works """
        self.stats.add_time(0.2222)
        super().assertListEqual([0.2222], self.stats.time_accumulator)

    def test_add_most_fitted(self):
        """ Most fitted accumulator works """
        expected = object.__new__(Individual)
        expected.__setattr__(self.fitness_value_literal, 0.5)

        self.stats.add_most_fitted(expected)
        super().assertListEqual([expected], self.stats.most_fitted_accumulator)

    def test_sum_aes(self):
        """ Time counter works """
        self.stats.sum_aes(2)
        self.stats.sum_aes(2)
        super().assertEqual(4, self.stats.aes_counter,)

    def test_reset(self):
        """ Reset stats method works """
        self.stats.aes_counter = 100
        self.stats.solution_found = True
        self.stats.reset()
        super().assertEqual(0, self.stats.aes_counter)
        super().assertEqual(False, self.stats.solution_found)

    def test_calculate_metrics(self):
        """ Calculate metrics works """
        self.stats.success_rate_accumulator = [1, 1, 1]
        self.stats.mbf_accumulator = [2, 2, 2]
        self.stats.aes_counter = 100
        self.stats.time_accumulator = [3, 3, 3]

        self.stats.calculate_metrics()

        super().assertEqual(1, self.stats.success_rate)
        super().assertEqual(2, self.stats.mbf)
        super().assertEqual(100, self.stats.aes)
        super().assertEqual(3, self.stats.mean_time)

    def test_get_most_fitted(self):
        """ Most fitted individual is found on most fitted accumulator """
        i1 = object.__new__(Individual)
        i1.__setattr__(self.fitness_value_literal, 0.01)
        i2 = object.__new__(Individual)
        i2.__setattr__(self.fitness_value_literal, 0.1)
        i3 = object.__new__(Individual)
        i3.__setattr__(self.fitness_value_literal, 0.001)

        mock_individual_list = list()

        mock_individual_list.append(i1)
        mock_individual_list.append(i2)
        mock_individual_list.append(i3)

        self.stats.most_fitted_accumulator = mock_individual_list

        super().assertEqual(self.stats.get_most_fitted(), i2)

    def test_avg(self):
        """ Average implementation works """
        test_list_1 = [1, 2, 3]
        super().assertEqual(2, self.stats.avg(test_list_1))

    def test_dict_and_repr(self):
        """ Checks that Stats instances are properly represented """
        stats_dict = {
            'success_rate': 1.0,
            'mbf': 0.5,
            'aes': 100,
            'mean_time': 4.5,
            'most_fitted': None
        }

        # Check that with no best individual representation is well formed
        stats = Stats()
        stats.success_rate = stats_dict['success_rate']
        stats.mbf = stats_dict['mbf']
        stats.aes = stats_dict['aes']
        stats.mean_time = stats_dict['mean_time']

        super().assertEqual(stats.__dict__, stats_dict)
        super().assertEqual(dict(stats), stats_dict)
        super().assertEqual(f'Stats({repr(stats_dict)})', repr(stats))

        # Check that with most fitted accumulator representation is well formed
        i = object.__new__(Individual)
        i.__setattr__(self.fitness_value_literal, 1.0)

        stats.most_fitted_accumulator = [i]
        stats_dict['most_fitted'] = i.__dict__

        super().assertDictEqual(stats_dict, stats.__dict__)
        super().assertEqual(stats_dict, dict(stats))
        super().assertEqual(f'Stats({repr(stats_dict)})', repr(stats))

    def test_persist(self):
        config = Config()
        config.report_format = ReportFormat.JSON
        config.report_path = self.test_report_path_file

        # When a best individual has been found
        i = object.__new__(Individual)
        i.__setattr__(self.fitness_value_literal, 1.0)
        self.stats.aes = 100
        self.stats.mbf = 0.9
        self.stats.mean_time = 0.42
        self.stats.success_rate = 1.0
        self.stats.most_fitted_accumulator = [i]
        self.stats.persist()

        with open(self.test_report_path_file, 'r') as persisted_report:
            red_report = persisted_report.readlines()

        super().assertEqual(str(dict(self.stats)) + '\n', red_report[0])

        # When a best individual has not been found
        self.stats.most_fitted_accumulator = []
        self.stats.persist()

        with open(self.test_report_path_file, 'r') as persisted_report:
            red_report = persisted_report.readlines()

        super().assertEqual(str(dict(self.stats)) + '\n', red_report[1])

    def test_to_csv(self):
        """ Test stats instance dict to csv conversion """
        with mock.patch('PatternOmatic.ge.stats.time') as mock_time:
            mock_time.return_value = .123
            self.stats.aes = 10
            self.stats.mbf = 0.5
            self.stats.mean_time = 0.22
            self.stats.success_rate = 0.5

            # When a best individual has not been found
            csv_stats = \
                f'{.123}\t{self.stats.mbf}\t{self.stats.success_rate}\t{self.stats.aes}\t{self.stats.mean_time}\t' \
                f'{None}\t'

            super().assertEqual(csv_stats, self.stats._to_csv())

            # When a best individual has been found
            i = object.__new__(Individual)
            i.__setattr__(self.fitness_value_literal, 1.0)
            self.stats.most_fitted_accumulator = [i]

            csv_stats += f'{None}\t{i.fitness_value}\t'
            super().assertEqual(csv_stats, self.stats._to_csv())

            # Also check csv is correctly persisted
            config = Config()
            config.report_path = self.test_report_path_file
            config.report_format = ReportFormat.CSV
            self.stats.persist()

            with open(self.test_report_path_file, 'r') as persisted_report:
                red_report = persisted_report.readlines()

            super().assertEqual(csv_stats + '\n', red_report[0])

    #
    # Helpers
    #
    def setUp(self) -> None:
        """ Fresh Stats instance """
        self.stats = Stats()
        if os.path.exists(self.test_report_path_file):
            os.remove(self.test_report_path_file)

    @classmethod
    def tearDownClass(cls) -> None:
        """ Remove temporary report file  """
        if os.path.exists(cls.test_report_path_file):
            os.remove(cls.test_report_path_file)

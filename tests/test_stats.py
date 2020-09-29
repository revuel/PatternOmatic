""" Unit testing file for stats module """
from unittest import TestCase, skip

from PatternOmatic.ge.stats import Stats


class IndividualMock(object):
    """ Mocks individual class just for fitness"""
    def __init__(self, fitness_value):
        self._fitness_value = fitness_value

    @property
    def __dict__(self):
        return {'most_fitted': {'FAKE_INDIVIDUAL': self.__class__.__name__, 'FAKE_FITNESS':  self._fitness_value}}

    @property
    def fitness_value(self):
        """ Fake fitness """
        return self._fitness_value


class TestStats(TestCase):
    """ Tests for Stats class """

    stats = None

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
        expected = IndividualMock(0.5)
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
        i1 = IndividualMock(0.01)
        i2 = IndividualMock(0.1)
        i3 = IndividualMock(0.001)

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

    @skip('Not implemented yet')
    def test_persist(self):
        self.fail()

    @skip('Not implemented yet')
    def test_to_csv(self):
        self.fail()

    #
    # Helpers
    #
    def setUp(self) -> None:
        """ Fresh Stats instance """
        self.stats = Stats()

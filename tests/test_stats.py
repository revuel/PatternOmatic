""" Unit testing file for stats module """
from unittest import TestCase, skip

from PatternOmatic.ge.stats import Stats


class IndividualMock(object):
    """ Mocks individual class just for fitness"""
    def __init__(self, fitness_value):
        self._fitness_value = fitness_value

    @property
    def fitness_value(self):
        return self._fitness_value


class TestStats(TestCase):
    """ Tests for Stats class """

    stats = None

    def test_add_sr(self):
        """ SR accumulator works """
        self.stats.add_sr(True)
        super().assertListEqual(self.stats.success_rate_accumulator, [True])

    def test_add_mbf(self):
        """ MBF acuumulator works """
        self.stats.add_mbf(0.5)
        super().assertListEqual(self.stats.mbf_accumulator, [0.5])

    def test_add_aes(self):
        """ AES accumulator works """
        self.stats.add_aes(10)
        super().assertListEqual(self.stats.aes_accumulator, [10])

    def test_add_time(self):
        """ Time accumulator works """
        self.stats.add_time(0.2222)
        super().assertListEqual(self.stats.time_accumulator, [0.2222])

    @skip('Not implemented yet')
    def test_add_most_fitted(self):
        self.fail()

    def test_sum_aes(self):
        """ Time counter works """
        self.stats.sum_aes(2)
        self.stats.sum_aes(2)
        super().assertEqual(self.stats.aes_counter, 4)

    def test_reset(self):
        """ Reset stats method works """
        self.stats.aes_counter = 100
        self.stats.solution_found = True
        self.stats.reset()
        super().assertEqual(self.stats.aes_counter, 0)
        super().assertEqual(self.stats.solution_found, False)

    @skip('Not implemented yet')
    def test_calculate_metrics(self):
        self.fail()

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
        """ Average implemntation works """
        test_list_1 = [1, 2, 3]
        super().assertEqual(self.stats.avg(test_list_1), 2)

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
        self.stats = Stats()

    def tearDown(self) -> None:
        self.stats = None

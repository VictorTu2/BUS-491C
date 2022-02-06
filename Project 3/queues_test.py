from unittest import TestCase
from unittest import main

import math

import queues as q


class Test_queues(TestCase):

    def setUp(self):
        self.lamda = 40.0
        self.mu = 50.0
        self.c = 1.0

    def test_is_valid(self):
        lamda = self.lamda
        mu = self.mu
        c = self.c

        # valid single valued lamda
        self.assertEqual(True, q.is_valid(lamda, mu))

        # test with non-positive arguments
        self.assertEqual(False, q.is_valid(0, mu, c))

        # test valid with multi-valued lamda (or at least lamda a tuple)
        self.assertEqual(True, q.is_valid((10, 20, 10), mu))

        # test invalid with multi-valued lamda
        self.assertEqual(False, q.is_valid((-10, 20, 10), mu, c))

    def test_is_feasible(self):

        lamda = self.lamda
        mu = self.mu
        c = self.c

        # test with valid queues, single-valued lamda
        self.assertEqual(True, q.is_feasible(40, 50))

        # test for invalid queues
        # test for non-positive arguments

        self.assertEqual(False, q.is_valid(0, mu, c))

        # test with non-numeric arguments
        self.assertEqual(False, q.is_feasible("twenty", mu, c))

        # test valid with multi-valued lamda (or at least lamda a tuple)
        self.assertEqual(True, q.is_feasible((10, 20, 10), mu))

        # test invalid with multi-valued lamda
        self.assertEqual(False, q.is_feasible((-10, 20, 10), mu, c))

    def test_calc_p0(self):

        lamda = self.lamda
        mu = self.mu
        c = self.c

        # test for valid queues, single valued lamda
        self.assertAlmostEqual(0.42857142857142855, q.calc_p0(40, 50, 2))

        # test for invalid queues
        self.assertTrue(math.isnan(q.calc_p0(0, 50, 2)))

        # test for infeasible queues
        self.assertTrue(math.isinf(q.calc_p0(lamda, lamda, c)))

        # test for valid queues, multi-valued lamda
        self.assertAlmostEqual(0.42857142857142855, q.calc_p0((10, 20, 10), 50, 2))

    def test_calc_lq_mmc(self):

        lamda = self.lamda
        mu = self.mu
        c = self.c

        # test valid results
        self.assertAlmostEqual(3.2, q.calc_lq_mmc(40, 50))

        # test invalid results

        self.assertTrue(math.isnan(q.calc_lq_mmc(0, 50, 2)))

        self.assertTrue(math.isnan(q.calc_lq_mmc(-lamda, mu, c)))

        # test infeasible queues
        self.assertTrue(math.isinf(q.calc_lq_mmc(lamda, lamda, c)))

        # test valid results with multiple classes
        self.assertAlmostEqual(.15238095238095242, q.calc_lq_mmc((10, 20, 10), 50, 2))


if __name__ == '__main__':
    rslt = main(verbosity=2, exit=False)

    print('done')







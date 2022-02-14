from unittest import TestCase
from unittest import main


import math

import queues as q

class Test_queues(TestCase):
    lamda = 0.0
    mu = 0.0
    c = 2.0

    def setUp(self):
        self.lamda = 40.0
        self.mu = 50.0
        self.c = 2.0

    def test_is_valid(self):
        lamda = self.lamda
        mu = self.mu
        c = self.c

        # valid single valued lamda
        self.assertEqual(True, q.is_valid(lamda, mu))

    def test_is_feasible(self):

        lamda = self.lamda
        mu = self.mu
        c = self.c

        # test with valid queues, single-valued lamda
        self.assertEqual(True, q.is_feasible(40, 50))

    def test_calc_p0(self):

        lamda = self.lamda
        mu = self.mu
        c = self.c

        # test for valid queues, single valued lamda
        self.assertAlmostEqual(0.42857142857142855, q.calc_p0(40, 50, 2))

    def test_calc_lq_mmc(self):

        lamda = self.lamda
        mu = self.mu
        c = self.c

        # test valid results
        self.assertAlmostEqual(3.2, q.calc_lq_mmc(40, 50))

    def test_calc_bk_mmc(self):
        k = 4
        self.assertAlmostEqual(1.0, q.calc_bk_mmc(0, (10, 20, 10), 50, 2))

    def test_calc_wqk_mmc(self):
        k = 4
        self.assertAlmostEqual(0.0036281179138322006, q.calc_wqk_mmc(2, (10, 20, 10), 50, 2))

    def test_calc_lqk_mmc(self):
        k = 6
        lamda = (20,30,40)
        wqk = q.calc_wqk_mmc(k, lamda, self.mu, 4)

        # validity checks
        self.assertTrue(math.isnan(q.calc_lqk_mmc(0, lamda, wqk)))

        # test with non-numeric arguments
        parms = [["one", 40, 50],
                 [2, "twenty", 50],
                 [2, 40, "twenty-five"],
                 ["one", "twenty", 50],
                 ["one", 40, "twenty-five"],
                 [2, "twenty", "twenty-five"],
                 ["one", "twenty", "twenty-five"]
        ]

        for k, lamda, wqk in parms:
            with self.subTest(k=k, lamda=lamda, wkq=wqk):
                self.assertTrue(math.isnan(q.calc_lqk_mmc(k, lamda, wqk)))

    def test_use_littles_law(self):
        lamda = 2
        mu = 4
        c = 6

        # using default values test default values for lamda, mu, and c (see setUp)

        # test all variations with a single server
        expected = { 'lq' : 6.4,
                     'l' : 8.0,
                     'wq' : 0.32,
                     'w' : 0.4,
                     'r' : 0.16,
                     'ro' : 0.16
                     }

        # test invalid call, no lq specified
        self.assertEqual(None,q.use_littles_law(self.lamda, self.mu, self.c))


if __name__ == '__main__':
    rslt = main(verbosity=2, exit=False)

    print('done')
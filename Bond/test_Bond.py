import BondYTM
import unittest
from datetime import date

class BondYTMTests(unittest.TestCase):
    def test_simpleBullet(self):
        valuationDate = date(2021,5,1)
        price = 1
        commission = 0.006
        couponSchedule = {date(2021,1,1): 0.1, date(2022,1,1): 0.1}
        sinkingSchedule = {date(2022,1,1): 1}
        self.assertAlmostEqual(BondYTM.BondYTM(valuationDate, price, commission, couponSchedule, sinkingSchedule), 0.093, delta=1e-8)

    def test_withSinkings(self):
        valuationDate = date(2021,5,1)
        price = 0.5
        commission = 0.006
        couponSchedule = {date(2021,1,1): 0.1, date(2022,1,1): 0.05}
        sinkingSchedule = {date(2021,1,1): 0.5, date(2022,1,1): 0.5}
        self.assertAlmostEqual(BondYTM.BondYTM(valuationDate, price, commission, couponSchedule, sinkingSchedule), 0.092, delta=1e-8)

    def test_withNegativeYTM(self):
        valuationDate = date(2021,5,1)
        price = 1.5
        commission = 0.006
        couponSchedule = {date(2021,1,1): 0.1, date(2022,1,1): 0.1}
        sinkingSchedule = {date(2022,1,1): 1}
        self.assertAlmostEqual(BondYTM.BondYTM(valuationDate, price, commission, couponSchedule, sinkingSchedule), -0.271, delta=1e-8)

if __name__ == "__main__":
    unittest.main()
from datetime import date
from math import isclose

def BondYTM():
    valuationDate = date(2021,5,1)
    couponSchedule = {date(2021,1,1): 0.1, date(2022,1,1): 0.1}
    sinkingSchedule = {date(2022,1,1): 1}
    rawPrice = 1
    commission = 0.006
    price = rawPrice * (1 + commission)

    (pastCoupons, coupons) = GetCoupons(couponSchedule, valuationDate)
    (pastSinkings, sinkings) = GetSinkings(sinkingSchedule, valuationDate)
    cashFlows = CalculateCashFlows(coupons, sinkings)
    ytm = CalculateYTM(cashFlows, price)
    return ytm


def GetCoupons(couponSchedule, valuationDate):
    (pastCoupons, coupons) = GetFlows(couponSchedule, valuationDate)
    return (pastCoupons, coupons)

def GetSinkings(sinkingSchedule, valuationDate):
    (pastSinkings, sinkings) = GetFlows(sinkingSchedule, valuationDate)
    return (pastSinkings, sinkings)

def GetFlows(schedule, valuationDate):
    pastFlows = {}
    flows = {}
    for (date, value) in schedule.items():
        if (date <= valuationDate):
            pastFlows[date] = value
        else:
            flows[date] = value
    return (pastFlows, flows)

def CalculateCashFlows(coupons, sinkings):
    cashFlows = {}
    for (couponDate, couponValue) in coupons.items():
        if (couponDate in cashFlows.keys()):
            cashFlows[couponDate] += couponValue
        else:
            cashFlows[couponDate] = couponValue
    for (sinkDate, sinkValue) in sinkings.items():
        if (sinkDate in cashFlows.keys()):
            cashFlows[sinkDate] += sinkValue
        else:
            cashFlows[sinkDate] = sinkValue
    return cashFlows

def CalculateYTM(cashFlows, price):
    ytm = 0.001
    n = 0
    while (n < 1_000_000):
        iterationPrice = CalculatePrice(cashFlows, ytm)
        if (isclose(iterationPrice, price, abs_tol=0.00101)):
            break
        ytm += 0.001
    return ytm

def CalculatePrice(cashFlows, ytm):
    # P = C1 / (1 + YTM)^1 + C2 / (1 + YTM)^2 + ... + Cn / (1 + YTM)^n + FV / (1 + YTM)^n
    price = 0.0
    n = 1
    for value in cashFlows.values():
        price += value / (1 + ytm)**n
        n += 1
    return price

print(BondYTM())
from sys import float_info as system
from math import isclose

def BondYTM(valuationDate, price, commission, couponSchedule, sinkingSchedule):
    price = price * (1 + commission)
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
    ytm = 0.0
    ytmStep = 0.001
    if (HasNegativeYTM(price, cashFlows)):
        ytmStep = -ytmStep
    
    maxIter = int(1/abs(ytmStep))
    priceTolerance = 0.0001
    n = 0
    success = False
    while (success is False):
        n += 1
        if (n == 10): break
        (success, ytm) = LookForYTM(price, cashFlows, ytmStep, priceTolerance, maxIter)
        priceTolerance *= 10
    return ytm

def HasNegativeYTM(price, cashFlows):
    a = abs(price - CalculatePrice(cashFlows, system.epsilon)) > abs(price - CalculatePrice(cashFlows, 0.0))
    return a

def LookForYTM(price, cashFlows, step, priceTolerance, maxIter):
    ytm = 0.0
    success = False
    for n in range(maxIter):
        iterationPrice = CalculatePrice(cashFlows, ytm)
        if (isclose(iterationPrice, price, abs_tol = priceTolerance)):
            success = True
            break
        ytm += step
    return (success, ytm)

def CalculatePrice(cashFlows, ytm):
    # P = C1 / (1 + YTM)^1 + C2 / (1 + YTM)^2 + ... + Cn / (1 + YTM)^n + FV / (1 + YTM)^n
    price = 0.0
    n = 1
    for value in cashFlows.values():
        price += value / (1 + ytm)**n
        n += 1
    return price
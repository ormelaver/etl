import statistics


def convertToFloat(numList):
    outList = []
    for i in range(len(numList)):
        try:
            outList.append(float(numList[i]))
        except ValueError:
            continue
    return outList

def calcMax(numList):
    return max(numList)

def calcMin(numList):
    return min(numList)

def calcAverage(numList):
    return statistics.mean(numList)

def calcMedian(numList):
    return statistics.median(numList)

def CalcAll(numList):
    return [str(calcMin(numList)), str(calcMax(numList)), str(calcAverage(numList)), str(calcAverage(numList))]
# import datetime
from datetime import datetime
from collections import OrderedDict
import os

def fileLen(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
        
def sortInts(nums):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(nums) - 1):
            try:
                if (nums[i] > nums[i + 1]):
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    swapped = True
            except Exception as e:
                print(e)
                continue
    return nums

def addMissingDates(dateList): 
    returnDict = dict()
    lastValue = dateList[len(dateList) - 1]
    for i in range(len(dateList) - 1):
        try:
            if (dateList[i + 1] - dateList[i] > 1):
                deficit = dateList[i + 1] - dateList[i]
                j = 1
                while j in range(deficit):
                    returnDict.update({dateList[i]: False})
                    returnDict.update({dateList[i] + j: True})
                    j += 1
            else:
                returnDict.update({dateList[i]: False}) 
        except Exception as e:
            returnDict.update({dateList[i]: False})
            print(e)
            continue
    
    returnDict.update({lastValue: False})
    return returnDict

def padAndSortDates(filePath):
    dates = []
    for line in filePath:
        try:
            dates.append(datetime.strptime(line.split(',')[0], "%Y-%m-%d"))
        except Exception as e:
            print(e, " - setting date value to 'N/A'")
            dates.append('N/A')
    for i in range(len(dates)):
        try:
            dates[i] = dates[i].toordinal()
        except Exception as e: print(e)
    sortInts(dates)
    paddedAndSorted = addMissingDates(dates)
    finalDict = {datetime.strftime(datetime.fromordinal(k), "%Y-%m-%d"): v for k, v in paddedAndSorted.items()}
    return finalDict

def cleanAndPadDates():
    dnldLocation = str(os.path.dirname(__file__))
    original = open(dnldLocation + '/rawNoTitle.csv', 'r+')
    paddedDates = padAndSortDates(original)
    original = open(dnldLocation + '/rawNoTitle.csv', 'r+')
    origDict = dict() 
    comboDict = dict()
    for line in original:
        origDict.update({line.split(',')[0]: line.split(',')[1]})
    for key in paddedDates.keys():
        for k in origDict.keys():
            if (paddedDates[key]):
                comboDict.update({key: 'N/A\n'})
            elif (key == k and not(paddedDates[key])):
                comboDict.update({key: origDict[key]})

    with open(dnldLocation + '/padded.csv', 'w') as padded:
        for key, value in comboDict.items():
            padded.writelines(key + ',' + value)
    original.close()
    


    

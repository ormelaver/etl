import requests
import dataUtilities
import os
import mathOps

def getData(url):
    try:

      print('Downloading source file...')
      dnldLocation = str(os.path.dirname(__file__))
      r = requests.get(url)
      # Retrieve HTTP meta-data
      print("success!", r.status_code)

      
      
      with open(dnldLocation + '/raw.csv', 'wb') as f:  
          f.write(r.content)
      f.close
    except Exception as e: print(e)

def cleanData(): 
    dnldLocation = str(os.path.dirname(__file__))
    with open(dnldLocation + '/raw.csv','r') as f:
        onlyData = open(dnldLocation + '/rawNoTitle.csv','w')
        next(f)
        for line in f:
            onlyData.write(line)
        onlyData.close()
        dataUtilities.cleanAndPadDates()


def doCalculations(granularity):
    allowedGns = {'weekly' : 7, 'hourly' : 7*24} ## add new gran here
    try:
        divider = allowedGns[granularity]
    except Exception as e: print(e)
                                                        
    dnldLocation = str(os.path.dirname(__file__))
    cleanFile = open(dnldLocation + '/padded.csv', 'r')
    currentPricesRaw = []
    lapse = 0
    final = open(dnldLocation + '/realFinal.csv', 'w+')
    final.writelines("DATE,CBETHUSD,lapse,low,high,average,median\n")
    lines = []
    shouldSkip = False
    fileLength = dataUtilities.fileLen(dnldLocation + '/padded.csv')

    for j, line in enumerate(cleanFile):
        price = line.split(',')[1]
        if (j % divider == 0 and not(shouldSkip) and j != fileLength - 1):
            currentPricesRaw.append(price)
            lines.append(line)
            shouldSkip = True
        elif ((j % divider == 0 and shouldSkip)):
            lapse += 1 
            shouldSkip = False
            currentPrices = mathOps.convertToFloat(currentPricesRaw)
            calculations = mathOps.CalcAll(currentPrices)
            currentPricesRaw = []
            currentPrices = []
            
            for l in lines:
                final.write(l + ',' + str(lapse) + ',' + ''.join(calculations) + '\n')
            
            lines = [line]
            if (fileLength - j < divider and j % divider == 0):
                currentPricesRaw.append(price)

        elif (fileLength - j + 1 < divider):
            lines.append(line)
            currentPricesRaw.append(price)
            
            
            if (fileLength - j == 1):
                lapse += 1
                currentPrices = mathOps.convertToFloat(currentPricesRaw)
                calculations = mathOps.CalcAll(currentPrices)
                for line in lines:
                    final.write(line + ',' + str(lapse) + ',' + ''.join(calculations) + '\n')

        elif (j % divider != 0):
            shouldSkip = True
            currentPricesRaw.append(price)
            lines.append(line)
    final.close()
    cleanFile.close() 

def deploy(url, inFile):
    r = requests.post(url, inFile)
    if (r.status_code == 200):
        print("file deployed successfully!", r.status_code, r.reason)
    else:
        print("error!", r.status_code, r.reason)
    
def main():
    getData('https://s3-eu-west-1.amazonaws.com/athena-dev-task/ETH_USD.csv')
    cleanData()
    doCalculations('weekly')
    deploy('https://s3-eu-west-1.amazonaws.com/athena-dev-task/OR_MELAVER/ETH_USD_agg.csv', str(os.path.dirname(__file__)) + '/realFinal.csv')
if __name__ == "__main__":
  main()
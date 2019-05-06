def loadData(fileName, features=[], labels=[]):
    fileOpen = open(fileName, "r")
    lines = fileOpen.readlines()
    fileOpen.close()
    for unFormattedLine in lines:
        line = unFormattedLine.split()
        currentLine = []
        for feature in line[:-1]:
            currentLine.append(float(feature))
        features.append(currentLine)
        labels.append(line[len(line)-1])

def reduceDuplicates(features=[], labels=[]):
    allValues = {}
    for column in range(len(features[0])):
        for row in range(len(features)):
            if features[row][column] not in allValues.keys():
                allValues[features[row][column]] = [0, 0]

            print(labels[row])
            if int(labels[row]) == int(1):
                print('label is 1')
                allValues[features[row][column]][0] += 1
            else :
                print('label is 0')
                allValues[features[row][column]][1] += 1
    return allValues
                
            

trainingSet = []
trainingLabels = []

# loadData('pa2train.txt', trainingSet, trainingLabels)
loadData('testing.txt', trainingSet, trainingLabels)
reducedList = reduceDuplicates(trainingSet, trainingLabels)

print(reducedList)
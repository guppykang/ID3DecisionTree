import collections
import math

class Node:
    def __init__(self, val):
        self.l = None
        self.r = None
        self.v = val

class Tree:
    def __init__(self, root=None):
        self.root = root

    def getRoot(self):
        return self.root

    def add(self, val):
        if(self.root == None):
            self.root = Node(val)
        else:
            self._add(val, self.root)

    def _add(self, val, node):
        if(val < node.v):
            if(node.l != None):
                self._add(val, node.l)
            else:
                node.l = Node(val)
        else:
            if(node.r != None):
                self._add(val, node.r)
            else:
                node.r = Node(val)

    def find(self, val):
        if(self.root != None):
            return self._find(val, self.root)
        else:
            return None

    def _find(self, val, node):
        if(val == node.v):
            return node
        elif(val < node.v and node.l != None):
            self._find(val, node.l)
        elif(val > node.v and node.r != None):
            self._find(val, node.r)

    def deleteTree(self):
        # garbage collector will do this for us. 
        self.root = None

    def printTree(self):
        if(self.root != None):
            self._printTree(self.root)

    def _printTree(self, node):
        if(node != None):
            self._printTree(Node(node).l)
            print(str(Node(node).v) + ' ')
            self._printTree(Node(node).r)


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


def reduceDuplicates(features, labels, feature):
    allValues = {}
    for row in range(len(features)):
        if features[row][feature] not in allValues.keys():
            allValues[features[row][feature]] = [0, 0]

        if int(labels[row]) == int(1):
            allValues[features[row][feature]][1] += 1
        else:
            allValues[features[row][feature]][0] += 1

    return collections.OrderedDict(sorted(allValues.items()))


def iterate(features=[], labels=[]):
    possibleSplits = []
    for i in range(len(features[0])):
        od = reduceDuplicates(features, labels, i)
        keys = od.keys()
        for split in range(len(keys)-1):
            #print('split after ' + str(split))
            middle = (keys[split] + keys[split+1])/2
            onesOnLeft = 0
            zerosOnLeft = 0
            onesOnRight = 0
            zerosOnRight = 0
            for leftIndex in range(split+1):
                onesOnLeft += od.get(keys[leftIndex])[1]
                zerosOnLeft += od.get(keys[leftIndex])[0]
            for rightIndex in range(split+1, len(keys)):
                onesOnRight += od.get(keys[rightIndex])[1]
                zerosOnRight += od.get(keys[rightIndex])[0]
            # print('zeros On left :' + str(zerosOnLeft))
            # print('ones On left :' + str(onesOnLeft))
            # print('zeros On right :' + str(zerosOnRight))
            # print('ones On right :' + str(onesOnRight))

            totalLeft = zerosOnLeft + onesOnLeft
            totalRight = zerosOnRight + onesOnRight
            total = totalRight + totalLeft

            probabilityOfLeftOne = float(onesOnLeft)/float(totalLeft)
            probabilityOfLeftZeros = float(zerosOnLeft)/float(totalLeft)
            left = 0.0
            right = 0.0
            if probabilityOfLeftOne != float(0):
                left = -1 * (probabilityOfLeftOne * math.log(probabilityOfLeftOne))
            if probabilityOfLeftZeros != float(0):
                right = -1 * (probabilityOfLeftZeros * math.log(probabilityOfLeftZeros))
            entropyOfLeft =  left + right


            probabilityOfRightOne = float(onesOnRight)/float(totalRight)
            probabilityOfRightZeros = float(zerosOnRight)/float(totalRight)

            left = 0.0
            right = 0.0
            if probabilityOfRightOne != float(0):
                left = -1*(probabilityOfRightOne * math.log(probabilityOfRightOne))
            if probabilityOfRightZeros != float(0):
                right = -1 *(probabilityOfRightZeros * math.log(probabilityOfRightZeros))
            entropyOfRight =  left + right


            totalEntropy = (float(totalLeft)/float(total))*entropyOfLeft + (float(totalRight)/float(total))*entropyOfRight
            # print(totalEntropy)

            #add the conditional entropy, the threshold, and the feature that we are splitting
            possibleSplits.append([totalEntropy, middle, i])

       
    possibleSplits.sort()
    print(possibleSplits)
    return possibleSplits[0]

def buildTree(root):
    bestSplit = iterate(root[0], root[1])

    leftChild = []
    rightChild = []

    foundMiddle = False
    middleIndex= 0

    for i in root[0]:
        if i[bestSplit[2]] >= bestSplit[1]:
            foundMiddle = True
            middleIndex = trainingSet.index(i) 
        if foundMiddle:
            break
        
    leftChild = [root[0][0:middleIndex], root[1][0:middleIndex]]
    rightChild = [root[0][middleIndex:], root[1][middleIndex:]]

    Node(root).l = Node(leftChild)
    Node(root).r = Node(rightChild)

    leftUniform = True
    for leftChildrenLabel in leftChild[1]:
        if leftChildrenLabel != leftChild[1][0]:
            leftUniform = False
            break

    rightUniform = True
    for rightChildrenLabel in rightChild[1]:
        if rightChildrenLabel != rightChild[1][0]:
            rightUniform = False
            break

    # if not leftUniform: 
    #     #recursive call on left
    # if not rightUniform:
    #     #recrusive call on right

    print(leftChild)
    print(rightChild)


# loadData('pa2train.txt', trainingSet, trainingLabels)
trainingSet = []
trainingLabels = []
loadData('testing.txt', trainingSet, trainingLabels)

#create the root 
yerMam = Tree([trainingSet, trainingLabels])

root = yerMam.root
buildTree(root)
print("Hi mom here's the tree")
yerMam.printTree()
    






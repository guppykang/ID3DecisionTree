import collections
import math
import Queue

class Node:
    def __init__(self, val):
        self.l = None
        self.r = None
        self.v = val
        self.isLeaf = False
        self.label = None
        self.rule = None
    
    def addLeft(self, data):
        self.l = Node(data)

    def addRight(self, data):
        self.r = Node(data)

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
            self._printTree(node.l)
            print(' leaf? ' + str(node.isLeaf) + '. predicting : ' + str(node.label) + ' with ' + str(len(node.v[0])) + ' nodes here')
            self._printTree(node.r)



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

        if int(float(labels[row])) == int(1):
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
    print('split at :' + str(possibleSplits[0]))
    return possibleSplits[0]



def buildTree(root):
    bestSplit = iterate(root.v[0], root.v[1])
    
    
    root.rule = bestSplit

    for y in range(len(root.v[0])):
        root.v[0][y].append(float(root.v[1][y]))
    root.v[0].sort(key  = lambda x: x[bestSplit[2]])
    
    for index in range(len(root.v[0])):
        root.v[1][index] = root.v[0][index][-1]
        root.v[0][index].pop(-1)

    leftChild = []
    rightChild = []

    foundMiddle = False
    middleIndex= 0

    for i in root.v[0]:
        if i[bestSplit[2]] >= bestSplit[1]:
            foundMiddle = True
            middleIndex = root.v[0].index(i) 
        if foundMiddle:
            # print('FOUND MIDDLE!!!!!!!!!!!!!!')
            # print('feature at index ' + str(middleIndex) + ' of value ' + str(i[bestSplit[2]]) + ' is greater than ' + str(bestSplit[1]))
            break
        
    leftChild = [root.v[0][0:middleIndex], root.v[1][0:middleIndex]]
    rightChild = [root.v[0][middleIndex:], root.v[1][middleIndex:]]

    root.addLeft(leftChild)
    root.addRight(rightChild)


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

    # print('left child : ' + str(leftChild))
    # print('right child : ' + str(rightChild))
    print('left child size ' + str(len(leftChild[0])))
    print('right child size ' + str(len(rightChild[0])))


    if leftUniform:
        root.l.isLeaf = True
        root.l.label = leftChild[1][0]
    if rightUniform:
        root.r.isLeaf = True
        root.r.label = rightChild[1][0]
    # print(str(root.l.v) + ' leaf? : ' + str(leftUniform) + '. predicting : ' + str(root.l.label))
    # print(str(root.r.v) + ' leaf? : ' + str(rightUniform) + '. predicting : ' + str(root.l.label))

    if not leftUniform:
        buildTree(root.l)
  

    if not rightUniform:
        buildTree(root.r)
    
def predict(root, x, list):
    #print('I am a leaf' + str(root.isLeaf) +  '. my rule is ' + str(root.rule) + '. my label is ' + str(root.label))

    if not root.isLeaf:
        if float(x[root.rule[2]]) < float(root.rule[1]):
            predict(root.l, x, list )
        else : 
            predict(root.r, x, list)
    list.append(root.label)

def printFirstThreeLevels(root):
    print('Root has ' + str(len(root.v[0])) + ' values in it and the splitting rule is ' + str(root.rule))
    print('Level 1 of nodes:')
    print('left node has ' + str(len(root.l.v[0])) + ' values in it and the splitting rule is ' + str(root.l.rule) + 'leaf node : ' + str(root.l.isLeaf) + ' label is : ' + str(root.l.label))
    print('right node has ' + str(len(root.r.v[0])) + ' values in it and the splitting rule is ' + str(root.r.rule) + 'leaf node : ' + str(root.r.isLeaf) + ' label is : ' + str(root.r.label))
    print('left left node has ' + str(len(root.l.l.v[0])) + ' values in it and the splitting rule is ' + str(root.l.l.rule) + 'leaf node : ' 
            + str(root.l.l.isLeaf) + ' label is : ' + str(root.l.l.label))
    print('left right node has ' + str(len(root.l.r.v[0])) + ' values in it and the splitting rule is ' 
            + str(root.l.r.rule) + 'leaf node : ' + str(root.l.r.isLeaf) + ' label is : ' + str(root.l.r.label))
    print('right left node has ' + str(len(root.r.l.v[0])) + ' values in it and the splitting rule is ' 
            + str(root.r.l.rule) + 'leaf node : ' + str(root.r.l.isLeaf) + ' label is : ' + str(root.r.l.label))
    print('right right node has ' + str(len(root.r.r.v[0])) + ' values in it and the splitting rule is ' 
            + str(root.r.r.rule) + 'leaf node : ' + str(root.r.r.isLeaf) + ' label is : ' + str(root.r.r.label))

def get_leaf_nodes(root):
    leaves = []
    _collect_leaf_nodes(root,leaves)
    return leaves

def _collect_leaf_nodes(node, leaves):
    if node is not None:
        if node.l is None and node.r is None:
            leaves.append(node)
        _collect_leaf_nodes(node.l, leaves)
        _collect_leaf_nodes(node.r, leaves)

def getValidationError(root, validationSet, validationLabels):
    numCorrect = 0
    for x in validationSet:
        guessList = []
        guess = predict(root, x, guessList)
        if float(guessList[0]) == float(validationLabels[validationSet.index(x)]):
            numCorrect += 1
    error = float(1000-numCorrect)/float(1000) 
    return error

def pruneLeftSubTree(root, validationSet, validationLabels, rootroot, ogRoot, previousRoot):
    oldNode = previousRoot.r

    if root[1] == 'left':
        print('left of : ')
        oldNode = previousRoot.l
    else : 
        print('right of : ')

    leaves = get_leaf_nodes(root[0])
    ones = 0
    zeros = 0

    for leaf in leaves:
        if float(leaf.label) == float(0):
            zeros += 1
        else :
            ones += 1
    
    consensus = -1
    if ones > zeros:
        consensus = 1.0
    else : 
        consensus = 0.0

    print('ones : ' + str(ones) + '. zeros : ' + str(zeros))
    print('consensus: ' + str(consensus))
    newNode = Node([[],[]])
    newNode.label = float(consensus)
    newNode.isLeaf = True

    if root[1] == 'left':
        previousRoot.l = newNode
    else: 
        previousRoot.r = newNode

    oldError = getValidationError(rootroot, validationSet, validationLabels)
    newError = getValidationError(ogRoot, validationSet, validationLabels)

    print('new error ' + str(error))
    print('old error ' + str(oldError))

    pruned = True

    if oldError < error:
        pruned = False
        if root[1] == 'left':
            previousRoot.l = oldNode
        else: 
            previousRoot.r = oldNode
    
    if root[1] == 'left':
        print('after ' + str((previousRoot.l.isLeaf)))
    else: 
        print('after ' + str((previousRoot.r.isLeaf)))
    
    return pruned

    

trainingLabels = []
trainingSet = []

#TRAINING DATA
loadData('pa2train.txt', trainingSet, trainingLabels)

#loadData('testing.txt', trainingSet, trainingLabels)
#loadData('inifniteLoop.txt', trainingSet, trainingLabels)

#TESTING DATA
testingSet = []
testingLabels= []
loadData('pa2test.txt', testingSet, testingLabels)
#testingSet = [[1, 0]]
#estingLabels = [1]

#VALIDATION DATA 
validationSet = []
validationLabels = []
loadData('pa2validation.txt', validationSet, validationLabels)

#create the root 
yerMam = Tree(Node([trainingSet, trainingLabels]))
tPrime = Tree(Node([trainingSet, trainingLabels]))
 

#BUILD TREE
root = yerMam.getRoot()
rootTPrime = tPrime.getRoot()

buildTree(root)
buildTree(rootTPrime)

print("Hi mom here's the tree")
yerMam.printTree()

#FIND ERROR
print('Hi mom im testing')
error = getValidationError(root, validationSet, validationLabels)
print('error ' + str(error))

#PRINT FIRST THREE LEVELS
printFirstThreeLevels(root)


#PRUNING STEP
q = Queue.Queue()
q.put([root.l, 'left'])
q.put([root.r, 'right'])

previous = root

#start from the left and rigth in the tree to begin with mate
while  not q.empty():
    currentSubTree = q.get()
    if currentSubTree[0].l is not None:
        q.put([currentSubTree[0].l, 'left'])
    if currentSubTree[0].r is not None: 
        q.put([currentSubTree[0].r, 'right'])

    #call the prune function   
    #prune on left and right sub tree
    # must first check to see if left subtree is not a leaf (and same for the right subtree)
    if currentSubTree[0] is not None and not currentSubTree[0].isLeaf:
        print(' subtree attempted pruning')
        leftIsPruned = pruneLeftSubTree(currentSubTree, validationSet, validationLabels, rootTPrime, root, previous)

    print('was pruned : ' + str(leftIsPruned))
    if leftIsPruned:
        rootTPrime = root
        break

    previous = currentSubTree[0]


print('Hi mom im testing : post pruning')
tError = getValidationError(rootTPrime, testingSet, testingLabels)
vError = getValidationError(rootTPrime, validationSet, validationLabels)
print('tError ' + str(tError))
print('vError ' + str(vError))





    
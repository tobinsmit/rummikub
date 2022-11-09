import numpy as np
import math
import sys

numberRange = range(13)
colorRange =['Red', 'Black', 'Blue', 'Yellow']

boardList = [
    (7, 'Red'),
    (8, 'Red'),
    (9, 'Red'),
]

hand = [
    (6, 'Red'),
    (8, 'Blue'),
]

def makeMatrix(boardList):
    matrix = np.zeros(shape=[len(colorRange), len(numberRange)], dtype=int)
    for tile in boardList:
        numIdx = tile[0]
        colIdx = colorRange.index(tile[1])
        matrix[colIdx, numIdx] += 1
    return matrix

testMatrix = makeMatrix(boardList)
print(testMatrix)

def checkPlanIsValid(plan):
    for group in plan:

        if len(group) < 3:
            pass
            return 'Group too short'

        numbersList = [tile[0] for tile in group]
        colorsList = [tile[1] for tile in group]
        numbersSet = set(numbersList)
        colorsSet = set(colorsList)

        isGroupOfNumbers = len(numbersSet) > 1
        isGroupOfColors = len(colorsSet) > 1

        if isGroupOfNumbers and isGroupOfColors:
            return 'Number group and color group'
        
        if isGroupOfNumbers:
            
            # Check numbers are consecutive
            sortedNumbers = np.sort(numbersList)
            sortedNumbersDiff = np.diff(sortedNumbers)
            if not np.all(sortedNumbersDiff == 1):
                return 'Number group not consecutive'

        if isGroupOfColors:
            if len(colorsSet) < len(colorsList):
                # There must be a color double up
                return 'Color group with double up'

    return True

# Testing checkPlanIsValid
assert checkPlanIsValid([ [(6, 'Red'), (7, 'Red'), (8, 'Red')] ]) == True, 'Does not work for normal group of numbers'
assert checkPlanIsValid([ [(10, 'Blue'), (10, 'Red'), (10, 'Black')] ]) == True, 'Does not work for normal group of colors'
assert checkPlanIsValid([ [(6, 'Red'), (7, 'Red'), (9, 'Red')] ]) != True, 'Does not catch gap in group of numbers'
assert checkPlanIsValid([ [(6, 'Red'), (7, 'Red'), (8, 'Blue')] ]) != True, 'Does not catch group with multiple numbers and multiple colors'
assert checkPlanIsValid([ [(6, 'Red'), (6, 'Red'), (7, 'Red')] ]) != True, 'Does not catch number group with double ups'
assert checkPlanIsValid([ [(10, 'Red'), (10, 'Red'), (10, 'Black')] ]) != True, 'Does not catch color group with double ups'
assert checkPlanIsValid([ [(10, 'Red'), (10, 'Black')] ]) != True, 'Does not catch color group with two tiles'
assert checkPlanIsValid([ [(6, 'Red'), (7, 'Red')] ]) != True, 'Does not catch number group with two tiles'
assert checkPlanIsValid([ [(num, 'Red') for num in numberRange] ]) == True, 'Does not allow large number group'
assert checkPlanIsValid([
    [(6, 'Red'), (7, 'Red'), (8, 'Red')],
    [(10, 'Blue'), (10, 'Red'), (10, 'Black'), (10,'Yellow')],
]) == True, 'Does not work with multiple  groups'
assert checkPlanIsValid([
    [(6, 'Red'), (7, 'Red'), (8, 'Red')],
    [(10, 'Red'), (10, 'Red')],
]) != True, 'Does not catch bad group in multiple groups'

def groupMapToPlan(tiles, groupMap):
    numGroups = max(groupMap)+1
    plan = [[] for _ in range(numGroups)]
    for tileIdx in range(len(groupMap)):
        groupIdx = groupMap[tileIdx]
        tile = tiles[tileIdx]
        plan[groupIdx].append(tile)

    return plan
    
tiles =  [
    (1, 'Red'),
    (2, 'Red'),
    (3, 'Red'),
    (10, 'Red'),
    (10, 'Black'),
    (10, 'Blue'),
]

groupMap = [
    0,
    0,
    0,
    1,
    1,
    1,
]

plan = groupMapToPlan(tiles, groupMap)
print(plan)

def solvePlanFromTilesWithBacktracking(tiles):
    groupMap = np.zeros(shape=np.size(tiles))
    currentTileIdx = 0
    velocity = 0
    numTiles = len(tiles)
    maxGroup = math.floor(numTiles/3)
    complete = False
    iterations = 0
    maxIterations = 1000
    while (currentTileIdx < numTiles) and (not complete) and (iterations < maxIterations):
        res = checkPlanIsValid(groupMapToPlan(tiles, groupMap))
        if res != True:
            currentGroup = groupMap[currentTileIdx]
            # if currentGroup == 

    if iterations == maxIterations:
        print('Maxed out on iterations')
    

def solvePlanFromTilesWithBruteForce(tiles):
    numTiles = len(tiles)
    numGroups = math.floor(numTiles/3)
    numIterations = numGroups ** numTiles
    print('numTiles', numTiles)
    print('numGroups', numGroups)
    print('numIterations', numIterations)
    solns = []
    for i in range(numIterations):
        groupMap = np.zeros(shape=[numTiles], dtype=np.int8)

        for tileIdx in range(numTiles):
            divisor = numGroups ** tileIdx
            premod = math.floor(i / divisor)
            group = premod % numGroups
            groupMap[tileIdx] = group

        # print(groupMap)
        if checkPlanIsValid(groupMapToPlan(tiles, groupMap)) == True:
            solns.append(groupMap)

    return solns

tiles =  [
    (6, 'Red'),
    (7, 'Red'),
    (8, 'Red'),
    (9, 'Red'),
    (10, 'Red'),
    (10, 'Yellow'),
    (10, 'Black'),
    (10, 'Blue'),
    (12, 'Blue'),
]

# solvePlanFromTilesWithBruteForce(tiles)

kernals = np.array([
    [
        [1,1,1,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
    ],
    [
        [0,1,1,1,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
    ],
    [
        [0,0,1,1,1],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
    ],
    [
        [0,0,1,0,0],
        [0,0,0,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
    ],
    [
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,0,0,0],
        [0,0,1,0,0],
    ],
    [
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,0,0,0],
    ],
])

def checkKernalsInMatrix(matrix, kernalIdxs, colorIdx, numberIdx):
    kernal = np.sum([kernals[kernalIdx] for kernalIdx in kernalIdxs], 0)
    for kernalRowIdx in range(len(kernal)):
        for kernalColIdx in range(len(kernal[0])):
            kernalVal = kernal[kernalRowIdx, kernalColIdx]
            if kernalVal > 0:
                matrixRowIdx = (kernalRowIdx + colorIdx) % len(colorRange)
                matrixColIdx = (kernalColIdx - 2 + numberIdx) % len(numberRange)
                matrixVal = matrix[matrixRowIdx, matrixColIdx]
                if matrixVal < kernalVal:
                    return False
    
    return True

def kernalToGroup(kernalIdx, colorIdx, numberIdx):
    kernal = kernals[kernalIdx]
    group = []
    for kernalRowIdx in range(len(kernal)):
        for kernalColIdx in range(len(kernal[0])):
            kernalVal = kernal[kernalRowIdx, kernalColIdx]
            if kernalVal > 0:
                matrixRowIdx = (kernalRowIdx + colorIdx) % len(colorRange)
                matrixColIdx = (kernalColIdx - 2 + numberIdx + len(numberRange)) % len(numberRange)
                color = colorRange[matrixRowIdx]
                number = numberRange[matrixColIdx]
                group.append((number, color))
    return group

def replace_submatrix(A, rows, cols, B):
  for idx, row in enumerate(rows):
    A[row, cols] = B[idx, :]
  return A
  
def kernalToMatrix(kernalIdx, colorIdx, numberIdx):
    kernal = np.array(kernals[kernalIdx], dtype=int)
    mat = np.zeros(shape=[len(colorRange), len(numberRange)], dtype=int)
    rows = (np.arange(len(kernal)) + colorIdx) % len(colorRange)
    cols = (np.arange(len(kernal[0])) - 2 + numberIdx + len(numberRange)) % len(numberRange)
    mat = replace_submatrix(mat, rows, cols, kernal)
    return mat


def find_options_matrix(matrix, colorIdx, numberIdx):
    new_groups = []
    for kernalIdx in range(len(kernals)):
        works = checkKernalsInMatrix(matrix, [kernalIdx], colorIdx, numberIdx)
        if works:
            group = kernalToGroup(kernalIdx, colorIdx, numberIdx)
            new_groups.append(group)


def find_options_plan(plan, colorIdx, numberIdx):
    group_option_idxs = []
    for group_idx, group in enumerate(plan):
        new_group = [*group, (numberIdx, colorRange[colorIdx])]
        if checkPlanIsValid([new_group]):
            group_option_idxs.append(group_idx)

    return group_option_idxs

def find_options(matrix, plan, colorIdx, numberIdx):
    mat_options = find_options_matrix(matrix, colorIdx, numberIdx)
    plan_options = find_options_plan(plan, colorIdx, numberIdx)
    return [*mat_options, *plan_options]

def solveMatrixAnalytically(matrix):
    plan = []
    just_made_changes = True
    optionsMat = np.zeros(shape=np.shape(matrix), dtype=int)
    while just_made_changes == True:
        just_made_changes = False

        # Check kernals on each tile
        for colorIdx in range(len(colorRange)):
            for numberIdx in range(len(numberRange)):
                quantityOfTile = matrix[colorIdx,numberIdx] # Is either 0, 1 or 2
                if quantityOfTile == 0:
                    continue

                options = find_options(matrix, plan, colorIdx, numberIdx)

                if len(options) == 0:
                    raise Exception('Tile has no options')

                elif len(options) == quantityOfTile:
                    # All options must be true
                    for option in options:
                        # Enact option
                        #TODO
                        pass
                        
                    just_made_changes = True
                        
                
                
    optionsMat[matrix == 0] = -1
    print("\n optionsMat")
    print(optionsMat)
    return (plan, matrix)

# matrix =  np.array([
#     # 1  2  3  4  5  6  7  8  9 10 11 12 13
#     [ 0, 2, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 2], # Red
#     [ 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2], # Black
#     [ 2, 1, 1, 1, 2, 0, 2, 1, 2, 0, 1, 1, 2], # Blue
#     [ 1, 0, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1], # Yellow
# ], dtype=int)
matrix =  np.array([
    # 1  2  3  4  5  6  7  8  9 10 11 12 13
    [ 0, 0, 1, 1, 1, 2, 1, 1, 0, 1, 2, 2, 1], # Red
    [ 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 2, 0, 1], # Black
    [ 2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 2, 2], # Blue
    [ 2, 1, 1, 0, 0, 0, 0, 1, 1, 1, 2, 1, 1], # Yellow
], dtype=int)

print('\n BEFORE')
print('matrix:')
print(matrix)
# print('plan:')
# print(plan)

(plan, leftover_matrix) = solveMatrixAnalytically(matrix)
# print('\n AFTER')
# print('matrix:')
# print(matrixAfter)
# print('plan:')
# print(planAfter)

import moment
numberOfUniqueTripletGroups = int(sum(sum(matrix)) / 3)
numberOfTests = 2 ** numberOfUniqueTripletGroups
print(f'The number of unique triplet groups is {numberOfUniqueTripletGroups} which would take {numberOfTests} tests')






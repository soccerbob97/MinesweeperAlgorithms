import json
import math
import numpy as np
from numpy import unravel_index
import os
import time
import glob

# Reveal a square on the visible board and update the probability of the surrounding squares
def visitSquare(row: int,  col: int):
    if (row < 0 or col < 0 or row >= height or col >= width):
        return
    if visibleBoard[row][col] == -1:
        coords.append((row, col))
        visibleBoard[row, col] = int(answerArray[row*width + col])

        probabilityBoard[row, col] = -9
        updateProbability(row, col)

        if(visibleBoard[row, col] == 9):
            global numBombs
            numBombs += 1
            global bombCoord
            bombCoord.append((row, col))

# Update the probability of the surrounding squares and mark off which squares we have visited already
def updateProbability(row: int, col: int):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (row+i, col+j) not in coords and not (row + i < 0 or col + j < 0 or row + i >= height or col + j >= width):
                if visibleBoard[row, col] == 0:
                    probabilityBoard[row + i, col + j] = -100
                elif not visibleBoard[row, col] == 9:
                    probabilityBoard[row + i, col +
                                     j] += visibleBoard[row, col]
                elif visibleBoard[row, col] == 9:
                    probabilityBoard[row + i, col + j] -= 2

# Calculate the distance to the center using pythagorean theorem
def distanceToCenter(row: int, col: int) -> int:
    val = (height/2 - row)**2 + (width / 2 - col)**2
    return math.sqrt(val)


stats_total = 0
stats_mined = 0
stats_bombs = 0
stats_boards = 0

path = os.path.dirname(os.path.abspath(__file__))
for filename in glob.glob(path + '/**/**'):

    if filename.endswith(".json"):
        bombCoord = []
        start = time.time()

        initial = json.loads(open(filename).read())

        # Initialize variables
        height, width = initial["dim"].split(",")
        height = int(height)
        width = int(width)
        maxNumBombs = initial["bombs"]
        safeSquare = initial["safe"]
        answerArray = initial["board"]

        # Initialize the board visible to the computer
        visibleBoard = np.empty(shape=(height, width))
        probabilityBoard = np.empty(shape=(height, width))
        visibleBoard.fill(-1)
        visibleBoard = visibleBoard.astype(int)

        # Initialize the probability board for decisions
        probabilityBoard = np.empty(shape=(height, width))
        probabilityBoard.fill(0)
        probabilityBoard = probabilityBoard.astype(int)
        finalBoard = [[int(answerArray[row*width + col])
                       for col in range(width)] for row in range(height)]
        answerKey = np.array(finalBoard)

        # Create local variables for specific board
        mined = 0
        maxCoords = []
        coords = []
        numBombs = 0

        print(filename)
        print(str(height) + ' x ' + str(width) +
              ' with ' + maxNumBombs + ' bombs')

        visitSquare(int(safeSquare.split(",")[0]), int(
            safeSquare.split(",")[1]))

        # While not all bombs have been found
        while(str(numBombs) != str(maxNumBombs)):
            minDistance = height + width
            xMax, yMax = np.where(probabilityBoard == np.max(probabilityBoard))

            # MinCoord is the square with the highest probability
            # and if there is a tie, it is the one closest to the center
            minCoord = ()
            for j in range(len(xMax)):
                if distanceToCenter(xMax[j], yMax[j]) < minDistance:
                    minDistance = distanceToCenter(xMax[j], yMax[j])
                    minCoord = (xMax[j], yMax[j])

            visitSquare(minCoord[0], minCoord[1])
            mined += 1

        # Calculate runtime of our algorithm
        runtime = int((time.time() - start) * 10000)

        # Print usefull statistics of our specific iteration
        print('Grid Area: ' + str(height*width) + ' squares')
        print('Bomb Density: ' + str(float(numBombs) /
              (height*width)) + ' bombs/square')
        print('Runtime: ' + str(float(runtime/100.0)) + ' seconds')
        print('Performance: ' + str(mined/float(height*width)) +
              ' percent of squares uncovered')
        print('Bomb Locations: ' + str(bombCoord))

        stats_total += height*width
        stats_mined += mined
        stats_bombs += numBombs
        stats_boards += 1
        print(' ')
        print(' ')
        print(' ')

avg_mined = float(stats_mined)/stats_total
print("Final stats: %d bombs found, %f percent mined on average across %d boards" %
      (stats_bombs, avg_mined, stats_boards))

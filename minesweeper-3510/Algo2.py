import json
import math
import numpy as np
from numpy import unravel_index
import os
import random
import sys
import time
import glob

# Makes sure that we only check inside the board scope
def inBounds(i, j):
    return (i >= 0 and j >= 0 and i < height and j < width)

# Reveal a square on the visible board
def visitSquare(row, col):
    val = answerKey[row][col]
    if (visibleBoard[row][col] == -1):
        visibleBoard[row][col] = val
        global mined
        mined += 1
        if(val == 9):
            global numBombs
            numBombs += 1
            global bombCoord
            bombCoord.append((row, col))


# Initialize variables for overall stats
stats_total = 0
stats_mined = 0
stats_bombs = 0
stats_boards = 0

# Find every single json file
path = os.path.dirname(os.path.abspath(__file__))
for filename in glob.glob(path + '/**', recursive=True):

    if filename.endswith(".json"):
        # Return list of bomb locations
        bombCoord = []

        # The starting time in order to keep track of runtime
        start = time.time()

        # Get specific json file
        initial = json.loads(open(filename).read())

        # Load parameters from the json file
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

        finalBoard = [[int(answerArray[row*width + col])
                       for col in range(width)] for row in range(height)]
        answerKey = np.array(finalBoard)

        # Create local variables for specific board
        mined = 0
        numBombs = 0

        print(filename)
        print(str(height) + ' x ' + str(width) +
              ' with ' + maxNumBombs + ' bombs')

        # Visit safe square
        visitSquare(int(safeSquare.split(",")[0]), int(
            safeSquare.split(",")[1]))

        # Visit every 'middle' square for each 3x3 grid that we create
        for row in range(1, height, 3):
            for col in range(1, width, 3):
                visitSquare(row, col)
                bombsInArea = 0

                # Get list of adjacent 8 squares
                coords = [(row + i, col + j)
                          for i in range(-1, 2) for j in range(-1, 2)]
                # print(coords)

                # While not all bombs in our sector have been uncovered
                # randomly choosean adjacent square until we have the right number of bombs
                while (bombsInArea != visibleBoard[row, col] and visibleBoard[row][col] != 9):
                    random.shuffle(coords)
                    visit = coords.pop()
                    if (inBounds(visit[0], visit[1])):
                        visitSquare(visit[0], visit[1])
                        if (visibleBoard[visit[0]][visit[1]] == 9):
                            bombsInArea += 1

                # If the middle square is a bomb, we must unfortunately mine out all
                # adjacent 8 squares as we do not know enough data
                if (visibleBoard[row][col] == 9):
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if (inBounds(row + i, col + j)):
                                visitSquare(row + i, col + j)

        # Extra Rows and Cols
        # This occurs if the height and width are not divisible by 3
        if (numBombs != maxNumBombs):
            # Extra rows

            if (height % 3 == 1):
                # Essentially perform the same process but now with an offset 3x3
                mod = height % 3
                for col in range(1, width, 3):
                    row = height - 2
                    visitSquare(height - 2, col)
                    # Create list of adjacent squares
                    coords = [(row + i, col + j)
                              for i in range(-1, 2) for j in range(-1, 2)]

                    bombsInArea = 0
                    while (bombsInArea != visibleBoard[row, col] and visibleBoard[row][col] != 9):
                        # Randomly pick an adjacent square until all bombs in 3x3 are found
                        random.shuffle(coords)
                        visit = coords.pop()
                        if (inBounds(visit[0], visit[1])):
                            visitSquare(visit[0], visit[1])
                            if (visibleBoard[visit[0]][visit[1]] == 9):
                                bombsInArea += 1
                    # If the middle is a 9, then we have no information about bombs in our grid and must
                    # mine everything
                    if (visibleBoard[row][col] == 9):
                        for i in range(-1, 2):
                            for j in range(-1, 2):
                                if (inBounds(row + i, col + j)):
                                    visitSquare(row + i, col + j)
                                    visitSquare(row + i, col + j)

        if (numBombs != maxNumBombs):
            # Extra cols

            if (width % 3 == 1):
                # Essentially perform the same process but now with an offset 3x3
                mod = width % 3
                for row in range(1, height, 3):
                    col = width - 2
                    visitSquare(row, col)
                    # Create list of adjacent squares
                    coords = [(row + i, col + j)
                              for i in range(-1, 2) for j in range(-1, 2)]

                    bombsInArea = 0
                    while (bombsInArea != visibleBoard[row, col] and visibleBoard[row][col] != 9):
                        # Randomly pick an adjacent square until all bombs in 3x3 are found
                        random.shuffle(coords)
                        visit = coords.pop()
                        if (inBounds(visit[0], visit[1])):
                            visitSquare(visit[0], visit[1])
                            if (visibleBoard[visit[0]][visit[1]] == 9):
                                bombsInArea += 1
                    # If the middle is a 9, then we have no information about bombs in our grid and must
                    # mine everything
                    if (visibleBoard[row][col] == 9):
                        for i in range(-1, 2):
                            for j in range(-1, 2):
                                if (inBounds(row + i, col + j)):
                                    visitSquare(row + i, col + j)

        # Last edge case, sometimes the bottom right square never gets checked:
        if (numBombs != maxNumBombs):
            visitSquare(height-1, width-1)

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

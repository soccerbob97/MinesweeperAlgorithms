import json
import math
import numpy as np
from numpy import unravel_index
import os
import random
import sys

initial =  json.loads(open('varied_size_boards/10rows_10cols_10d_0.json').read())

height,width = initial["dim"].split(",")
height = int(height)
width = int(width)
maxNumBombs = initial["bombs"]
safeSquare = initial["safe"]
answerArray = initial["board"]

# Initialize the board visible to the computer
visibleBoard =  np.empty(shape=(height,width))
probabilityBoard =  np.empty(shape=(height,width))
visibleBoard.fill(-1)
visibleBoard = visibleBoard.astype(int)

finalBoard = [[int(answerArray[row*width + col]) for col in range(width)] for row in range(height)]
answerKey = np.array(finalBoard)

mined = 0
numBombs = 0

def inBounds(i,j) :
    return ( i >= 0 and j >= 0 and  i < height and  j < width)

def visitSquare(row, col) :
    val = answerKey[row][col]
    if (visibleBoard[row][col] == -1):
        visibleBoard[row][col] = val
        global mined
        mined += 1
        if(val == 9):
            global numBombs
            numBombs += 1

visitSquare(int(safeSquare.split(",")[0]),int(safeSquare.split(",")[1]))

for row in range(1,height,3):
    for col in range(1,width,3):
        visitSquare(row,col)
        bombsInArea = 0

        # Get list of adjacent 8 squares
        coords = [(row + i, col + j) for i in range(-1,2)  for j in range(-1,2)]
        print(coords)

        # While not all bombs in our sector have been uncovered
        # randomly choosean adjacent square until we have the right number of bombs
        while (bombsInArea != visibleBoard[row,col] and visibleBoard[row][col] != 9):
            random.shuffle(coords)
            visit = coords.pop()
            visitSquare(visit[0],visit[1])
            if (visibleBoard[visit[0]][visit[1]] == 9):
                bombsInArea +=1

        # If the middle square is a bomb, we must unfortunately mine out all 
        # adjacent 8 squares as we do not know enough data
        if (visibleBoard[row][col] == 9):
            for i in range (-1,2):
                for j in range(-1,2):
                    visitSquare(row + i, col + j)
        
        # Extra Rows and Cols
        # This occurs if the height and width are not divisible by 3

print (numBombs)
print(maxNumBombs)
print(mined)
        

print(visibleBoard)
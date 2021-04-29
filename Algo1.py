import json
import math
import numpy as np
from numpy import unravel_index
import os


stats_total = 0
stats_mined = 0
stats_bombs = 0
stats_boards = 0
path = '/Users/armaanlala/Developer/Minesweeper-Algorithms/varied_size_boards'

for filename in os.listdir(path):
    
    if filename.endswith(".json"): 

        initial = json.loads(open("varied_size_boards/" + filename).read())
        

        height,width = initial["dim"].split(",")
        height = int(height)
        width = int(width)
        maxNumBombs = initial["bombs"]
        safeSquare = initial["safe"]
        answerArray = initial["board"]

        visibleBoard =  np.empty(shape=(height,width))
        probabilityBoard =  np.empty(shape=(height,width))
        visibleBoard.fill(-1)
        visibleBoard = visibleBoard.astype(int)

        probabilityBoard =  np.empty(shape=(height,width))
        probabilityBoard.fill(0)
        probabilityBoard = probabilityBoard.astype(int)
        #temp variable
        finalBoard = [[int(answerArray[j*width + i]) for i in range(width)] for j in range(height)]
        answerKey = np.array(finalBoard)

        max = 0
        for row in answerKey:
            for val in row:
                if val > max and val < 9:
                    max = val
        # print(max)


        coords = []
        numBombs = 0

        def visitSquare(x: int,  y: int):
            
            if (x < 0 or y < 0 or x >= height or y>= width):
                return
            if visibleBoard[x][y] == -1:
                coords.append((x,y))
                visibleBoard[x,y]  = int(answerArray[x*width + y])

                probabilityBoard[x,y] = -9
                updateProbability(x,y)

                if(visibleBoard[x,y]  == 9):
                    global numBombs
                    numBombs+=1
                # print(visibleBoard[x,y])


        def updateProbability(x: int, y:int): 
            
            for i in range(-1,2):
                for j in range(-1,2):
                    if (x+i,y+j) not in coords and not (x + i < 0 or y + j < 0 or x + i >= height or y + j>= width):
                        if visibleBoard[x,y] == 0:
                            probabilityBoard[x + i, y + j] = -100
                        elif not visibleBoard[x,y] == 9:
                            probabilityBoard[x + i, y + j] += visibleBoard[x,y]
                        elif visibleBoard[x,y] == 9:
                            probabilityBoard[x + i, y + j] -= 2

        def distanceToCenter(x:int , y:int) -> int:
            val = (height/2 - x)**2 + (width /2 - y)**2
            return math.sqrt(val)

        visitSquare(int(safeSquare.split(",")[0]),int(safeSquare.split(",")[1]))

        maxCoords = []

        mined = 0
        while(str(numBombs) != str(maxNumBombs)):
        # for i in range(3):
            minDistance = height + width
            xMax,yMax = np.where(probabilityBoard == np.max(probabilityBoard))

            minCoord = ()
            for j in range(len(xMax)):
                if distanceToCenter(xMax[j],yMax[j]) < minDistance:
                    minDistance = distanceToCenter(xMax[j],yMax[j])
                    minCoord = (xMax[j],yMax[j])

            visitSquare(minCoord[0],minCoord[1])
            mined += 1

        print(str(numBombs) + ' bombs. Mined ' + str(mined) + ' out of ' + str(height*width))
        stats_total += height*width 
        stats_mined += mined
        stats_bombs += numBombs
        stats_boards += 1

avg_mined = float(stats_mined)/stats_total
print("Final stats: %d bombs found, %f percent mined on average across %d boards"  % (stats_bombs,avg_mined,stats_boards))
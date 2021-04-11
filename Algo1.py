import json
import numpy as np

# initial = json.loads(open('deterministic_board.json').read())
initial = json.loads(open('test_board.json').read())

height,width = initial["dim"].split(",")
height = int(height)
width = int(width)
numBombs = initial["bombs"]
safeSquare = initial["safe"]
answerArray = initial["board"]

visibleBoard =  np.empty(shape=(height,width))
visibleBoard.fill(-1)
visibleBoard = visibleBoard.astype(int)

#temp variable
finalBoard = [[int(answerArray[i*width + j]) for i in range(height)] for j in range(width)]
answerKey = np.array(finalBoard)

def visitSquare(x: int,  y: int):
    if (x < 0 or y < 0 or x >= width or y>= height):
        return
    if visibleBoard[x][y] == -1:
        visibleBoard[x][y] = answerKey[x][y]
        if (visibleBoard[x][y] == 0):
            for i in range(-1,2):
                for j in range(-1,2):
                    try:
                        visitSquare(x+i,y+j)
                    except:
                        return
        elif (visibleBoard[x][y] == 9):
            print("bomb")

visitSquare(int(safeSquare[0]),int(safeSquare[2]))
print(visibleBoard)
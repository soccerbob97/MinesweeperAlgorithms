import json
import numpy as np

# initial = json.loads(open('deterministic_board.json').read())
initial = json.loads(open('standard_boards/varied_density/20x_20y_02d_0.json').read())

height,width = initial["dim"].split(",")
height = int(height)
width = int(width)
numBombs = initial["bombs"]
safeSquare = initial["safe"]
answerArray = initial["board"]
print(safeSquare)

visibleBoard =  np.empty(shape=(height,width))
visibleBoard.fill(-1)
visibleBoard = visibleBoard.astype(int)

#temp variable
finalBoard = [[int(answerArray[j*width + i]) for i in range(width)] for j in range(height)]
answerKey = np.array(finalBoard)

max = 0
for row in answerKey:
    for val in row:
        if val > max and val < 9:
            max = val
print(max)

def visitSquare(x: int,  y: int):
    if (x < 0 or y < 0 or x >= width or y>= height):
        return
    if visibleBoard[x][y] == -1:
        visibleBoard[x,y]  = int(answerArray[y*width + x])
        print(visibleBoard[x,y])

visitSquare(int(safeSquare[0]),int(safeSquare[2]))

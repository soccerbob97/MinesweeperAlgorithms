import json
import numpy as np

# initial = json.loads(open('deterministic_board.json').read())
initial = json.loads(open('test_boards/varied_size/10_10_10.json').read())

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

def visitSquare(x: int,  y: int):
    # x = width - x
    # y =  height - y
    if (x < 0 or y < 0 or x >= width or y>= height):
        return
    if visibleBoard[x][y] == -1:
    #     visibleBoard[x][y] = finalBoard[x][y]
        visibleBoard[x,y] = answerKey[x,y]
        # visibleBoard[x,y]  = int(answerArray[y*width + x])
        print(visibleBoard[x,y])




visitSquare(int(safeSquare[0]),int(safeSquare[2]))


print(answerKey)
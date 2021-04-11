import json
import numpy as np

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

finalBoard = [[int(answerArray[i*width + j]) for i in range(height)] for j in range(width)]
answerArray = np.array(finalBoard)


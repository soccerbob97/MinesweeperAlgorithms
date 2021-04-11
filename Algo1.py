import json

initial = json.loads(open('test_board.json').read())

height,width = initial["dim"].split(",")
height = int(height)
width = int(width)
numBombs = initial["bombs"]
safeSquare = initial["safe"]
answerArray = initial["board"]

visibleBoard = [[-1]*height]*width
answerBoard = [[-1]*height]*width

for index in range(height*width):
    answerBoard[index%height][int(index/height)] = answerArray[index]

# print(answerArray)
# for i in range (height):
#     for j in range (width):
#         # print("i " + i)
#         # print("j " + j)
#         #print((i * width) + j)
#         # print(answerArray[(i * width) + j])
#         # val = answerArray[(i * width) + j]
#         # print(val)
#         # answerBoard[i][j] = val
#         # print (answerBoard)
#         answerBoard[i][j] = answerArray[(i * height) + j]

print(answerBoard)
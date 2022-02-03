import os
from numpy import Infinity


def drawBoard(board):
    e = ["X", "-", "O"]
    print("")
    for y in range(0, 6):
        line_str = ""
        for x in range(0, 7):
            line_str+="%s " %(e[board[y*7+x]+1])
        print(line_str)

def placeChip(board, player, column):
    if(board[column] == 0):
        for i in range(0, 6):
            if(board[column + i*7] == 0):
                continue
            else:
                board[column + (i-1)*7] = player
                return
        board[column + i*7] = player
            
def getChildren(board, player):
    children = []
    for i in range(0, 7):
        if(board[i] == 0):
            temp = board[:]
            placeChip(temp, player, i)
            children.append(temp)
    return children

def checkColumn(board):
    for x in range(0, 7):
        for y in range(0, 3):
            index = y*7+x
            if(board[index] != 0):
                if(board[index] == board[index+7] 
                == board[index+14] == board[index+21]):
                    return True

def checkRow(board):
    for y in range(0, 6):
        for x in range(0, 4):
            index = y*7+x
            if(board[index] != 0):
                if(board[index] == board[index+1] 
                == board[index+2] == board[index+3]):
                    return True

def checkDiagonal(board):
    global diagonal
    for c in diagonal:
        if(board[c[0]] != 0):
            if(board[c[0]] == board[c[1]] 
            == board[c[2]] == board[c[3]]):
                return True

def calculateEval(tuple):
    eval = 0
    playerAmount, computerAmount = 0, 0
    for e in tuple:
        if(e == -1): playerAmount+=1
        elif(e == 1): computerAmount+=1
    
    if(playerAmount > 0 and playerAmount < 4 and computerAmount > 0 and computerAmount < 4):
        if(playerAmount+computerAmount == 4):
            return 0
    
    if(playerAmount == 1): eval-=1
    elif(playerAmount == 2): eval-=10
    elif(playerAmount == 3): eval-=100
    elif(playerAmount == 4): eval-=1000

    if(computerAmount == 1): eval+=1
    elif(computerAmount == 2): eval+=10
    elif(computerAmount == 3): eval+=100
    elif(computerAmount == 4): eval+=1000

    return eval


def isOver(board):
    if(checkRow(board) or checkColumn(board) or checkDiagonal(board) or availabeMoves(board) == 0):
        return True

def rateBoard(board):
    global diagonal
    eval = 0
    
    # column
    for x in range(0, 7):
        for y in range(0, 3):
            index = y*7+x
            if(board[index] != 0):
                eval += calculateEval((board[index], board[index+7], board[index+14], board[index+21]))
    # row
    for y in range(0, 6):
        for x in range(0, 4):
            index = y*7+x
            if(board[index] != 0):
                eval += calculateEval((board[index], board[index+1], board[index+2], board[index+3]))
    # diagonal
    for c in diagonal:
        if(board[c[0]] != 0):
            eval += calculateEval((board[c[0]], board[c[1]], board[c[2]], board[c[3]]))

    return eval

def availabeMoves(board):
    moves = 0
    for e in board:
        if(e == 0): moves+=1
    return moves

def minimax(board, depth, alpha, beta, maximizing):
    if(depth == 0 or isOver(board)):
        return rateBoard(board)
    
    if maximizing:
        maxEval = -Infinity
        b_children = getChildren(board, 1)
        for child in b_children:
            eval = minimax(child, depth-1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = +Infinity
        b_children = getChildren(board, -1)
        for child in b_children:
            eval = minimax(child, depth - 1, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def genMove(board):
    b_children = getChildren(board, 1)
    maximum, index = -Infinity, 0
    for i in range(0, len(b_children)):
        eval = minimax(b_children[i], 5, -Infinity, +Infinity, False)
        if(eval > maximum): maximum, index = eval, i
    return b_children[index]

def getInput(board):
    pInput = input("Where to place chip? (1-7)" + "\n")
    pInput = int(pInput)-1
    placeChip(board, -1, pInput)

diagonal =  [(14, 22, 30, 38), (7, 15, 23, 31), (15, 23, 31, 39), (0, 8, 16, 24), (8, 16, 24, 32), (16, 24, 32, 40), 
            (1, 9, 17, 25), (9, 17, 25, 33), (17, 25, 33, 41), (2, 10, 18, 26), (10, 18, 26, 34),(3, 11, 19, 27), 
            (20, 26, 32, 38), (13, 19, 25, 31), (19, 25, 31, 37), (6, 12, 18, 24), (12, 18, 24, 30), (18, 24, 30, 36), 
            (5, 11, 17, 23), (11, 17, 23, 29), (17, 23, 29, 35), (4, 10, 16, 22), (10, 16, 22, 28), (3, 9, 15, 21)]

b= [0, 0, 0, 0, 0, 0, 0,    #  0,  1,  2,  3,  4,  5,  6
    0, 0, 0, 0, 0, 0, 0,    #  7,  8,  9, 10, 11, 12, 13
    0, 0, 0, 0, 0, 0, 0,    # 14, 15, 16, 17, 18, 19, 20
    0, 0, 0, 0, 0, 0, 0,    # 21, 22, 23, 24, 25, 26, 27
    0, 0, 0, 0, 0, 0, 0,    # 28, 29, 30, 31, 32, 33, 34
    0, 0, 0, 0, 0, 0, 0]    # 35, 36, 37, 38, 39, 40, 41

while 1:
    if(isOver(b)): break

    drawBoard(b)

    getInput(b)

    if(isOver(b)): break

    drawBoard(b)

    b = genMove(b)

drawBoard(b)

print("Game finished!")

os.system("pause")
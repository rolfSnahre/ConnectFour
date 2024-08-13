import functools
import random
from typing import Callable, Optional

NUM_COLLUMS = 7
NUM_ROWS = 6

def createGame():
    return [[0 for _ in range(NUM_ROWS)] for _ in range(NUM_COLLUMS)]

def possibleActions(gameState):
    return [i for i in range(NUM_COLLUMS) if gameState[i][-1] == 0 ]

def placePice(gameState, collum, player):
    row = 0
    firstAvailable = -1

    while row < len(gameState[collum]) and firstAvailable == -1:
        if gameState[collum][row] == 0:
            gameState[collum][row] = player
            firstAvailable = row
        row = row + 1  

    pos = (collum, firstAvailable)
    return gameState, pos

def gameStateToDisplayString(gameState):
    LINE_LENGHT=29
    horisontalLine = functools.reduce(lambda c, s: s + c, ['-' for _ in range(LINE_LENGHT)])
    display = horisontalLine + "\n" 
    for row in reversed(range(NUM_ROWS)):
        for collum in range(len(gameState)):
            display = display + "| " + str(gameState[collum][row]) + " "
        display = display + "|"
        display = display + "\n" + horisontalLine + "\n"
     
    
    return display

def displayWholeGame(winner, gameStates):
    for gameState in gameStates:
        print(gameStateToDisplayString(gameState))
    print("Player " + str(winner) + " won")

def checkVictory(gamestate, pos):
    #         |      --     /       \
    dirs = [(0,1), (1,0), (1,1), (1, -1)]
    return any(check4GivenLine(gamestate, pos, dir) for dir in dirs)


def check4GivenLine(gamestate, pos, dir):
    num_from_side_1 = numberConnectedInDir(gamestate, pos, dir)
    reversed_dir = (-dir[0], -dir[1])
    num_from_side_2 = numberConnectedInDir(gamestate, pos, reversed_dir)
    # -1 because pos is countet twice (both when checking dir and reveres_dir)
    return (num_from_side_1 + num_from_side_2 - 1) >= 4 

def outOfBound(pos):
    x, y = pos
    return x <0 or x >= NUM_COLLUMS or y<0 or y >= NUM_ROWS     

# includes original position
# dir is vector descibing how the x and y emlements increment when moving in that direction [1,1] is diagonaly upwards
def numberConnectedInDir(gamestate, pos, dir):
    player = gamestate[pos[0]][pos[1]]
    total_connected = 1
    correct_player = True
    out_of_bound = False
    pos_to_check = pos
    while correct_player and not(out_of_bound):
        pos_to_check = (pos_to_check[0] + dir[0], pos_to_check[1] + dir[1])
        if outOfBound(pos_to_check):
            out_of_bound = True
        elif gamestate[pos_to_check[0]][pos_to_check[1]] != player:
            correct_player = False
        else:
            total_connected = total_connected + 1
    return total_connected



def randomPlayerTurn(gamestate, posible_actions):
    return posible_actions[random.randint(0,len(posible_actions)-1)]

def play(player1_maketurn_func = randomPlayerTurn, player2_maketurn_func = randomPlayerTurn):
    gameState = createGame()
    winner = -1
    current_player = 1
    turn_funcs = {1 : player1_maketurn_func, 2 : player2_maketurn_func }
    gameStates = [gameState]
    turns = []
    while winner == -1:
        possible_actions = possibleActions(gameState)
        collum_chosen = turn_funcs[current_player](gameState, possible_actions)
        
        if collum_chosen not in possible_actions:
            print("Pice can not be placed in filled collum")
            return (winner, gameStates, turns)
        
        gameState, pos =  placePice(gameState, collum_chosen, current_player)
        gameStates.append(gameState)
        turns.append(collum_chosen)
        
        if checkVictory(gameState, pos):
            winner = current_player
        
        if current_player == 1:
            current_player = 2
        else:
            current_player = 1
        
            
    
    return winner, gameStates, turns



    
winner, gameStates, turns = play()
displayWholeGame(winner, gameStates)

print("Turns: " + str(turns))
print()



    
""" game = createGame()
game = placePice(game, 1, 1)
game = placePice(game, 1, 2)
game = placePice(game, 1, 1)

display = gameStateToDisplayString(game)

print(display)
a = 1 """



#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import time
import random

#customizable variables. Note that tkinter measures buttonwidth/height in character lengths and pillow uses pixels to measure it's distances. You can use ratio to do this.
circlewidth = 80 #change this value to increase the horizontal size.
circleheight = 80 #change this value to increase the verticle size.
ratio = 25
buttonwidth = circlewidth*2//ratio
buttonheight = circleheight//ratio
    
class GameState:
    def __init__(self):
        self.turn = 1
        self.current_move = 1
        self.board = [[0 for i in range(6)] for j in range(7)]
        self.height = [0 for i in range(7)]
        self.move_list = ""
        self.gamespeed = "slow"
        self.animationspeed = 0.125
        self.computerplayers = []
        self.gameon = 1

class ComputerPlayer:
    def __init__(self,filename,computertype):
        with open(filename,'r') as f:
            text = f.read()
        texts = text.split("¬")
        co1 = texts[0].split("_")
        self.columntypegames = [i.split("-") for i in co1]
        ro1 = texts[1].split("_")
        self.rowtypegames = [i.split("-") for i in ro1]
        di1 = texts[2].split("_")
        self.diagonaltypegames = [i.split("-") for i in di1]
        co2 = texts[3].split("_")
        self.columntypescore = [i.split("-") for i in co2]
        ro2 = texts[4].split("_")
        self.rowtypescore = [i.split("-") for i in ro2]
        di2 = texts[5].split("_")
        self.diagonaltypescore = [i.split("-") for i in di2]
        self.columntype = [[int(10**(float(self.columntypescore[i][j])/float(self.columntypegames[i][j])*10))for j in range(16)] for i in range(4)]
        self.rowtype = [[int(10**(float(self.rowtypescore[i][j])/float(self.rowtypegames[i][j])*10)) for j in range(289)] for i in range(6)]
        self.diagonaltype = [[int(10**(float(self.diagonaltypescore[i][j])/float(self.diagonaltypegames[i][j])*10)) for j in range(len(self.diagonaltypescore[i]))] for i in range(6)]
        self.computertype = computertype
        
comp1 = ComputerPlayer('connecttrainingvalues','unsupervised')

        
def train(computer): #Train the computer values using the most recent games.
    position = [[0 for j in range(6)] for i in range(7)] #position over the course of the game.
    fposition = [[0 for j in range(6)] for i in range(7)] #inverted position.
    height = [0 for i in range(7)]
    print(connect.move_list)
    if connect.turn == 2:
        result = 1
    else:
        result = 2*((connect.turn)%2) #result == 2 is a yellow win, result == 0 is a red win, and result == 1 is a draw.
    for i,j in enumerate(connect.move_list):
        move = int(j)
        size_factor = 0.9**(len(connect.move_list) - move - 1) #To give less weighting to moves played earlier in the game.
        position[move][height[move]] = 2-(i%2) 
        fposition[move][height[move]] = 1+(i%2)
        column_indexr = takecolumn([position[move][k] for k in range(6)])
        column_indexy = takecolumn([fposition[move][k] for k in range(6)])
        if move < 4:
            m = move
        else:
            m = 6 - move
        computer.columntypescore[m][column_indexr] = str(round(float(computer.columntypescore[m][column_indexr]) + (2 - result)*size_factor,3)) #add a value between 0 and 2 to the total score.
        computer.columntypescore[m][column_indexy] = str(round(float(computer.columntypescore[m][column_indexy]) + result*size_factor,3))
        computer.columntypegames[m][column_indexr] = str(round(float(computer.columntypegames[m][column_indexr]) + 2*size_factor,3)) #add the maximum possible score that could have been achieved to the games.
        computer.columntypegames[m][column_indexy] = str(round(float(computer.columntypegames[m][column_indexy]) + 2*size_factor,3))
        row_indexr = takerow([position[k][height[move]] for k in range(7)]) 
        row_indexy = takerow([fposition[k][height[move]] for k in range(7)])
        computer.rowtypescore[height[move]][row_indexr] = str(round(float(computer.rowtypescore[height[move]][row_indexr]) + (2 - result)*size_factor,3))
        computer.rowtypescore[height[move]][row_indexy] = str(round(float(computer.rowtypescore[height[move]][row_indexy]) + result*size_factor,3))
        computer.rowtypegames[height[move]][row_indexr] = str(round(float(computer.rowtypegames[height[move]][row_indexr]) + 2*size_factor,3))
        computer.rowtypegames[height[move]][row_indexy] = str(round(float(computer.rowtypegames[height[move]][row_indexy]) + 2*size_factor,3))
        diagonals_index = [diagonals.index(diagonal) for diagonal in diagonals if (move,height[move]) in diagonal] 
        for k in diagonals_index:
            diagonal1_indexr = takediagonal([position[l[0]][l[1]] for l in diagonals[k]])
            diagonal1_indexy = takediagonal([fposition[l[0]][l[1]] for l in diagonals[k]])
            computer.diagonaltypescore[k//2][diagonal1_indexr] = str(round(float(computer.diagonaltypescore[k//2][diagonal1_indexr]) + (2 - result)*size_factor,3))
            computer.diagonaltypescore[k//2][diagonal1_indexy] = str(round(float(computer.diagonaltypescore[k//2][diagonal1_indexy]) + result*size_factor,3))
            computer.diagonaltypegames[k//2][diagonal1_indexr] = str(round(float(computer.diagonaltypegames[k//2][diagonal1_indexr]) + 2*size_factor,3))
            computer.diagonaltypegames[k//2][diagonal1_indexy] = str(round(float(computer.diagonaltypegames[k//2][diagonal1_indexy]) + 2*size_factor,3))
        height[move] += 1
    with open('connecttrainingvalues','w') as f:
        f.write("_".join(["-".join(i) for i in computer.columntypegames]) + "¬" + "_".join(["-".join(i) for i in computer.rowtypegames]) + "¬" + "_".join(["-".join(i) for i in computer.diagonaltypegames])
            + "¬" + "_".join(["-".join(i) for i in computer.columntypescore]) + "¬" + "_".join(["-".join(i) for i in computer.rowtypescore]) + "¬" + "_".join(["-".join(i) for i in computer.diagonaltypescore]))
    computer.columntype = [[int(10**(float(computer.columntypescore[i][j])/float(computer.columntypegames[i][j])*10))for j in range(16)] for i in range(4)]
    computer.rowtype = [[int(10**(float(computer.rowtypescore[i][j])/float(computer.rowtypegames[i][j])*10)) for j in range(289)] for i in range(6)]
    computer.diagonaltype = [[int(10**(float(computer.diagonaltypescore[i][j])/float(computer.diagonaltypegames[i][j])*10)) for j in range(len(computer.diagonaltypescore[i]))] for i in range(6)]

def takediagonal(vector): #finds the identifier for a diagonal of the position.
    if len(vector) == 4:
        if 2 in vector:
            return 16
        return vector[0] + vector[1]*2 + vector[2]*4 + vector[3]*8
    if len(vector) == 5:
        if 2 in vector[1:4]:
            return 64
        if not 2 in vector:
            return vector[0] + vector[1]*2 + vector[2]*4 + vector[3]*8 + vector[4]*16
        if vector[0] == 2:
            if vector[4] == 2:
                return 64
            return 32 + vector[1] + vector[2]*2 + vector[3]*4 + vector[4]*8
        return 32 + 16 + vector[0] + vector[1]*2 + vector[2]*4 + vector[3]*8
    if 2 in vector[2:4]:
        return 176
    if vector[1] == 2:
        vector[0] = 2
    if vector[4] == 2:
        vector[5] = 2
    if len([2 for i in vector if i == 2]) > 2:
        return 176
    if not 2 in vector:
        return vector[0] + vector[1]*2 + vector[2]*4 + vector[3]*8 + vector[4]*16 + vector[5]*32
    if vector[0] == 2:
        if vector[1] != 2:
            if vector[5] != 2:
                return 64 + vector[1] + vector[2]*2 + vector[3]*4 + vector[4]*8 + vector[5]*16
            return 64 + 32 + 32 + vector[1] + vector[2]*2 + vector[3]*4 + vector[4]*8
        return 64 + 32 + 32 + 16 + vector[2] + vector[3]*2 + vector[4]*4 + vector[5]*8
    if vector[4] != 2:
        return 64 + 32 + vector[0] + vector[1]*2 + vector[2]*4 + vector[3]*8 + vector[4]*16
    return 64 + 32 + 32 + 16 + 16 + vector[0] + vector[1]*2 + vector[2]*4 + vector[3]*8

def takecolumn(vector): #finds the identifier for a column of the position.
    if 2 in vector[2:6]:
        return 15
    if vector[1] == 2:
        vector[0] = 2
    count_opp = len([2 for i in vector if i == 2])
    count_pla = len([1 for i in vector if i == 1])
    return count_opp*5 + count_pla

def takerow(vector): #finds the identifier for a row of the position.
    if vector[3] == 2:
        return 288
    if vector[2] == 2:
        vector[1] = 2
    if vector[1] == 2:
        vector[0] = 2
    if vector[4] == 2:
        vector[5] = 2
    if vector[5] == 2:
        vector[6] = 2
    if len([2 for i in vector if i == 2]) > 3:
        return 288
    weight = sum([10 + j*0.1 if k == 2 else k for j,k in enumerate(vector[:3])] + [-10 - j*0.1 if k == 2 else -k for j,k in enumerate(vector[4:])])
    if weight < 0:
        vector.reverse()
    if vector[0] != 2:
        return vector[0] + vector[1]*2 + vector[2]*4 + vector[3]*8 + vector[4]*16 + vector[5]*32 + vector[6]*64
    if vector[1] != 2:
        if vector[6] != 2:
            return 128 + vector[1] + vector[2]*2 + vector[3]*4 + vector[4]*8 + vector[5]*16 + vector[6]*32
        return 128 + 64 + vector[1] + vector[2]*2 + vector[3]*4 + vector[4]*8 + vector[5]*16
    if vector[2] != 2 and vector[6] != 2:
        return 128 + 64 + 32 + vector[2] + vector[3]*2 + vector[4]*4 + vector[5]*8 + vector[6]*16
    if vector[2] != 2:
        return 128 + 64 + 32 + 32 + vector[2] + vector[3]*2 + vector[4]*4 + vector[5]*8
    return 128 + 64 + 32 + 32 + 16 + vector[3] + vector[4]*2 + vector[5]*4 + vector[6]*8

def evaluation(position,player,column_changes,row_changes,diagonal_changes,previous_red_index,previous_yellow_index): #given a player and a position, evaluate the activity for that player.
    if player == 2:
        index = previous_yellow_index.copy()
        new_position = [[3 - position[i][j] if position[i][j] != 0 else 0 for j in range(6)] for i in range(7)]
    else:
        index = previous_red_index.copy()
        new_position = position
    for i in column_changes:
        index[i] = takecolumn([new_position[i][j] for j in range(6)])
    for i in row_changes:
        index[i+7] = takerow([new_position[j][i] for j in range(7)])
    if diagonal_changes:
        for i in diagonal_changes:
            index[13+i] = takediagonal([new_position[k[0]][k[1]] for k in diagonals[i]])   
    return index
    
def getvalue(new_position,turnn,new_moves,previous_red_score,previous_yellow_score,previous_red_index,previous_yellow_index,computer): #calculates the final score of a position. (operates with respect to a previously calculated position)
    diagonal_changes = {diagonals.index(diagonal) for i in new_moves for diagonal in diagonals if i in diagonal}
    column_changes = {i[0] for i in new_moves}
    row_changes = {i[1] for i in new_moves}
    red_index = evaluation(new_position,1,column_changes,row_changes,diagonal_changes,previous_red_index,previous_yellow_index)
    yellow_index = evaluation(new_position,2,column_changes,row_changes,diagonal_changes,previous_red_index,previous_yellow_index)
    red_score = previous_red_score
    yellow_score = previous_yellow_score
    for i in column_changes:
        if i < 4:
            red_score = red_score + computer.columntype[i][red_index[i]] - computer.columntype[i][previous_red_index[i]]
            yellow_score = yellow_score + computer.columntype[i][yellow_index[i]] - computer.columntype[i][previous_yellow_index[i]]
        else:
            red_score += computer.columntype[6-i][red_index[i]] - computer.columntype[6-i][previous_red_index[i]]
            yellow_score += computer.columntype[6-i][yellow_index[i]] - computer.columntype[6-i][previous_yellow_index[i]]
    for i in row_changes:
        red_score += computer.rowtype[i][red_index[i+7]] - computer.rowtype[i][previous_red_index[i+7]]
        yellow_score += computer.rowtype[i][yellow_index[i+7]] - computer.rowtype[i][previous_yellow_index[i+7]]
    for i in diagonal_changes:
        red_score += computer.diagonaltype[i//2][red_index[i+13]] - computer.diagonaltype[i//2][previous_red_index[i+13]]
        yellow_score += computer.diagonaltype[i//2][yellow_index[i+13]] - computer.diagonaltype[i//2][previous_yellow_index[i+13]]
    score = round((red_score - yellow_score)/(red_score + yellow_score + 0.0001),3)
    if turnn == 0:
        score = -score
    return score, red_score,yellow_score,red_index,yellow_index

def treep(computer):
    if connect.gamespeed != "super":
        treebutton.configure(bg ='dark grey')
    window.update_idletasks()
    for button in button_list:
        button.configure(command = 'none')
    previous_red_score = 249975 #The initial value of the board with blank rows, columns and diagonals having computer value = 0.5. (calculated as 25*10**5 - 25)
    previous_yellow_score = 249975
    previous_red_index = [0 for i in range(25)] #Indexes corresponding to the blank board.
    previous_yellow_index = [0 for i in range(25)]
    moves = [(i,j) for i in range(7) for j in range(6)] #Tell getvalue() to investigate the entire board for differences between the blank board and current position.
    t,previous_red_score,previous_yellow_score,previous_red_index,previous_yellow_index = getvalue(connect.board,connect.turn,moves,previous_red_score,previous_yellow_score,previous_red_index,previous_yellow_index,computer)
    height = [len([1 for j in range(6) if connect.board[i][j] != 0]) for i in range(7)]
    value, values = tree(height,previous_red_score,previous_yellow_score,previous_red_index,previous_yellow_index,computer)
    ki = random.randint(0,11110) #play a non-optimal move sometimes.
    if ki < 10000:
        move = random.choice([i for i in range(7) if values[i] == max(values)])
    elif ki < 11000:
        move = random.choice([i for i in range(7) if values[i] >= max(values) - abs(max(values))/4])
    elif ki < 11100:
        move = random.choice([i for i in range(7) if values[i] >= max(values) - abs(max(values))/2])
    elif ki < 11110:
        move = random.choice([i for i in range(7) if values[i] >= max(values) - abs(max(values))])
    elif ki < 11111:
        move = random.choice([i for i in range(7) if values[i] != -2]) #-2 is the value given to a filled column.
    if connect.gamespeed != "super":
        treebutton.configure(bg='#F0F0F0')
    place(move)
    for i,button in enumerate(button_list):
        button.configure(command = lambda e=i:place(e))
    
def tree(height,previous_red_score,previous_yellow_score,previous_red_index,previous_yellow_index,computer):
    turnn = connect.turn
    new_position = [[connect.board[i][j] for j in range(6)] for i in range(7)]
    values = [[[[2 for _ in range(7)] for o in range(7)] for u in range(7)]for t in range(7)]
    values1 = [-2 for _ in range(7)]
    values2 = [[2 for _ in range(7)] for o in range(7)]
    values3 = [[[-2 for _ in range(7)] for o in range(7)] for u in range(7)]
    for i in range(7):
        if height[i] < 6:
            new_position[i][height[i]] = turnn + 1
            value,first_red_score,first_yellow_score,first_red_index,first_yellow_index = getvalue(new_position,turnn,[(i,height[i])],previous_red_score,previous_yellow_score,previous_red_index,previous_yellow_index,computer)
            height[i] += 1
            if value < -0.95: #override the search tree if the first move is winning.
                values1[i] = 0.98
            else:
                turnn = 1 - turnn
                for j in range(7):
                    if height[j] < 6:
                        new_position[j][height[j]] = turnn + 1
                        value,second_red_score,second_yellow_score,second_red_index,second_yellow_index = getvalue(new_position,turnn,[(j,height[j])],first_red_score,first_yellow_score,first_red_index,first_yellow_index,computer)
                        height[j] += 1
                        if value < -0.95: #override the search tree if the second move is winning.
                            values2[i][j] = -0.98
                        else:
                            turnn = 1 - turnn
                            for k in range(7):
                                if height[k] < 6:
                                    new_position[k][height[k]] = turnn + 1
                                    value,third_red_score,third_yellow_score,third_red_index,third_yellow_index = getvalue(new_position,turnn,[(k,height[k])],second_red_score,second_yellow_score,second_red_index,second_yellow_index,computer)
                                    height[k] += 1
                                    if value < -0.95: #override the search tree if the third move is winning.
                                        values3[i][j][k] = 0.99
                                    else:
                                        turnn = 1 - turnn
                                        for l in range(7):
                                            if height[l] < 6:
                                                new_position[l][height[l]] = turnn + 1
                                                if i > k and not j in [i,k]:
                                                    values[i][j][k][l] = values[k][j][i][l]
                                                elif j > l and not k in [l,j]:
                                                    values[i][j][k][l] = values[i][l][k][j]
                                                else:
                                                    values[i][j][k][l],q,w,e,r  = getvalue(new_position,turnn,[(l,height[l])],third_red_score,third_yellow_score,third_red_index,third_yellow_index,computer)
                                                new_position[l][height[l]] = 0
                                        values3[i][j][k] = min(values[i][j][k])
                                        if values3[i][j][k] == -2:
                                            values3[i][j][k] = 0
                                        turnn = 1 - turnn
                                    height[k] -= 1
                                    new_position[k][height[k]] = 0
                            turnn = 1 - turnn
                            values2[i][j] = max(values3[i][j])
                            if values2[i][j] == 2:
                                values2[i][j] = 0
                        height[j] -= 1
                        new_position[j][height[j]] = 0
                turnn = 1 - turnn
                values1[i] = min(values2[i])
                if values1[i] == -2:
                    values1[i] = 0
            height[i] -= 1
            new_position[i][height[i]] = 0
    return 0, values1

def place(move): #runs every time a move is played.
    if connect.height[move] < 6: #a move can be played if the column has fewer than 6 pieces in it.
        if connect.gamespeed in ["slow","very slow"]: #if gamespeed is "slow", disable user input and play the animation.
            for button in button_list:
                button.configure(command = 'none')
            button_list[move].configure(bg = ['red','yellow'][connect.turn])
            button_list[move].flash()
            button_list[move].configure(bg = '#F0F0F0')
            for i in range(6 - connect.height[move]):
                label_list[(move)*6 + i].configure(image=imgs[connect.turn])
                window.update()
                label_list[(move)*6 + i].configure(image=imgs[2])
                time.sleep(connect.animationspeed)
        if connect.gamespeed != "super":
            label_list[(move)*6 + 5 - connect.height[move]].configure(image=imgs[connect.turn])
            for i,button in enumerate(button_list):
                button.configure(command = lambda e=i: place(e))
        connect.board[move][connect.height[move]] = connect.turn + 1
        connect.move_list += str(move)
        connect.height[move] += 1
        if checkvictory((move,connect.height[move] - 1)):
            gameover(connect.turn)
            return
        if 0 not in [connect.board[i][j] for i in range(7) for j in range(6)]:
            gameover(-1)
            return
        switchturn()
        window.update_idletasks()
        if connect.turn in connect.computerplayers: #check if the computer is the next player to move.
            treep(comp1)

def switchturn(): #general updates after a move has been made.
    connect.turn = -(connect.turn-1)
    connect.current_move += 1
    playerturn.configure(bg = ['red','yellow'][connect.turn])
    turnnumber.configure(text = "Turn " + str(connect.current_move))
    
def check4inrow(vector): #Given a line on the board, checks if 4 are the turn player's colour.
    numinrow = 0
    for i in vector:
        if i == connect.turn + 1:
            numinrow += 1
            if numinrow == 4:
                return True
        else:
            numinrow = 0
    return False

def checkvictory(move): #Finds the rows, columns and diagonals around the move played, and runs check4inrow to see if there are 4 in a row.
    if check4inrow(connect.board[move[0]]):
        return True
    if check4inrow([connect.board[i][move[1]] for i in range(7)]):
        return True
    diagonal_checks = [diagonal for diagonal in diagonals if move in diagonal]
    if diagonal_checks:
        for diagonal in diagonal_checks:
            if check4inrow([connect.board[point[0]][point[1]] for point in diagonal]):
                return True
    return False

def gameover(turn): #Performs actions for after a win or a draw.
    connect.current_move = len(connect.move_list)
    if connect.gamespeed in ["slow","very slow"]:
        winner = "winner!"
        if turn == -1:
            winner = " draw! "
        for i in range(7):
            button_list[i].configure(command = 'none',text = winner[i],bg = ['red','yellow','#F0F0F0'][turn])
            button_list[i].flash()
            button_list[i].configure(activebackground = ['red','yellow','#F0F0F0'][turn])
    gamechosen()
    resetbutton.grid(row=8,column=3)
    beginbutton.grid(row=8,column=1)
    backwardmovebutton.grid(row=8,column=2)
    forwardmovebutton.grid(row=8,column=4)
    endbutton.grid(row=8,column=5)
    compfirstbutton.configure(state='active',bg = '#F0F0F0')
    compsecondbutton.configure(state='active',bg = '#F0F0F0')
    treebutton.configure(state='active',command='none',bg = '#F0F0F0')
    twoplayerbutton.configure(state='active',bg = '#F0F0F0')
    self_playbutton.configure(state='active',bg = '#F0F0F0')
    readgamebutton.configure(state='active',bg = '#F0F0F0')
    connect.computerplayers = []
    connect.gameon = 0
    train(comp1)

def resetboard(): #Resets the board to its beginning state.
    resetbutton.grid_forget()
    beginbutton.grid_forget()
    backwardmovebutton.grid_forget()
    forwardmovebutton.grid_forget()
    endbutton.grid_forget()
    for i in range(6):
        for j in range(7):
            label_list[j*6 + i].configure(image = imgs[2])
    for i in range(7):
        button_list[i].configure(bg = '#F0F0F0', activebackground = '#F0F0F0', command = lambda e=i: place(e), text = '')
    connect.board = [[0 for i in range(6)] for j in range(7)]
    treebutton.configure(state='active',command=lambda e=comp1:treep(e),bg = '#F0F0F0')
    turnnumber.configure(text = "Turn 1")
    playerturn.configure(bg = 'yellow')
    connect.turn = 1
    connect.current_move = 1
    connect.move_list = ""
    connect.height = [0 for i in range(7)]
    connect.gameon = 1

def switchgamespeed():
    if connect.gamespeed == "super":
        connect.gamespeed = "fast"
        speedtogglebutton.configure(text = "fast")
        for i in range(7):
            for j in range(6):
                label_list[i*6 + 5 - j].configure(image = imgs[(connect.board[i][j]-1)%3])
    elif connect.gamespeed == "fast":
        connect.gamespeed = "slow"
        speedtogglebutton.configure(text = "slow")
    elif connect.animationspeed == 0.125:
        connect.animationspeed = 0.25
        connect.gamespeed = "very slow"
        speedtogglebutton.configure(text = "very slow")
    else:
        connect.animationspeed = 0.125
        connect.gamespeed = "super"
        speedtogglebutton.configure(text = "invisible")
        for i in range(42):
            label_list[i].configure(image = imgs[2])

def readgame():
    readgamebutton.configure(bg = 'dark grey')
    text = gameentryentry.get()
    if text:
        connect.move_list = text
        y = connect.gamespeed
        connect.gamespeed = "fast"
        gameover(-1)
        connect.gamespeed = y
        tobegin()

def tobegin(): #resets the game position after a game for inspection and analysis.
    connect.height = [0 for i in range(7)]
    connect.current_move = 0
    connect.board = [[0 for i in range(6)] for j in range(7)]
    for i in range(6):
        for j in range(7):
            label_list[(i)*7 - 1 + j].configure(image=imgs[2])

def forwardmove(): #panels forwards through the game.
    if connect.current_move < len(connect.move_list):
        add = int(connect.move_list[connect.current_move])
        connect.board[add][connect.height[add]] = (connect.current_move+1)%2 + 1
        if connect.gamespeed == "slow":
            for i in range(5 - connect.height[add]):
                label_list[(add)*6 + i].configure(image=imgs[(connect.current_move+1)%2])
                window.update_idletasks()
                label_list[(add)*6 + i].configure(image=imgs[2])
                time.sleep(connect.animationspeed)
        label_list[(add)*6 + 5 - connect.height[add]].configure(image=imgs[(connect.current_move+1)%2])
        connect.current_move += 1
        connect.height[add] += 1

def backwardmove(): #panels backwards through the game.
    if connect.current_move > 0:
        connect.current_move -= 1
        sub = int(connect.move_list[connect.current_move])
        connect.height[sub] -= 1
        connect.board[sub][connect.height[sub]] = 0
        label_list[(sub)*6 + 5 - connect.height[sub]].configure(image=imgs[2])

def toend(): #resets the game position to the end of the game.
    connect.height = [0 for i in range(7)]
    connect.board = [[0 for j in range(6)] for i in range(7)]
    for i,j in enumerate(connect.move_list):
        move = int(j)
        connect.board[move][connect.height[move]] = i%2+1
        label_list[move*6 + 5 - connect.height[move]].configure(image=imgs[(i+1)%2])
        connect.height[move] += 1
    connect.current_move = len(connect.move_list)
        
def self_play():
    num_of_games = self_playentry.get()
    if num_of_games == "":
        num_of_games = "1"
        self_playentry.insert(0,"1")
    if connect.gameon == 0:
        resetboard()
    if str.isdigit(num_of_games):
        self_playbutton.configure(bg='dark grey')
        window.update_idletasks()
        gamechosen()
        treebutton.configure(state='active',command='none')
        st1 = time.time()
        move_list = connect.move_list
        for _ in range(int(num_of_games)):
            resetboard()
            for i in move_list: #if self_play is run, it starts every game from the board position before it was pressed.
                place(int(i))
            connect.computerplayers = [0,1]
            treep(comp1) #since connect.computerplayers is [0,1], treep() will loop itself until the game ends, due to the callback at the end of place().
        en1 = time.time()
        print(f"time taken: {en1 - st1}")

def compfirst():
    compfirstbutton.configure(bg = 'dark grey')
    connect.computerplayers = [1]
    if connect.gameon == 0:
        resetboard()
    gamechosen()
    if connect.turn == 1:
        treep(comp1)
    
def compsecond():
    compsecondbutton.configure(bg = 'dark grey')
    connect.computerplayers = [0]
    if connect.gameon == 0:
        resetboard()
    gamechosen()
    if connect.turn == 0:
        treep(comp1)
    
def twoplayer():
    twoplayerbutton.configure(bg = 'dark grey')
    if connect.gameon == 0:
        resetboard()
    gamechosen()
    
def gamechosen():
    compfirstbutton.configure(state='disabled')
    compsecondbutton.configure(state='disabled')
    treebutton.configure(state='disabled')
    twoplayerbutton.configure(state='disabled')
    self_playbutton.configure(state='disabled')
    readgamebutton.configure(state='disabled')

#setting up global variables.
connect = GameState()
#setting up piece images in pillow. Blue backgrounds form the board. A circle is of the desired colour is drawn ontop to create each state of the board.
window = tk.Tk() #A tkinter window must be present for ImageTk.PhotoImage.
im = Image.new('RGB', (circlewidth,circleheight), (100,100,255))#'blue')
im2 = Image.new('RGB', (circlewidth,circleheight), (100,100,255))#'blue')
im3 = Image.new('RGB', (circlewidth,circleheight),(100,100,255))#'blue')
draw = ImageDraw.Draw(im)
draw = draw.ellipse((circlewidth//10,circleheight//10,9*circlewidth//10,9*circleheight//10), fill = 'red', outline = 'red')
draw2 = ImageDraw.Draw(im2)
draw2 = draw2.ellipse((circlewidth//10,circleheight//10,9*circlewidth//10,9*circleheight//10), fill = 'yellow', outline = 'yellow')
draw3 = ImageDraw.Draw(im3)
draw3 = draw3.ellipse((circlewidth//10,circleheight//10,9*circlewidth//10,9*circleheight//10), fill = (240,240,240), outline = (100,100,255))#'blue')
img = ImageTk.PhotoImage(im)
img2 = ImageTk.PhotoImage(im2)
img3 = ImageTk.PhotoImage(im3)
imgs = [img,img2,img3]
    
#setting up tkinter window and widgets.

playerturn = tk.Label(window, bg = 'yellow',height=buttonheight,width=buttonwidth)
playerturn.grid(row=8,column=0)
turnnumber = tk.Label(window,text = "Turn 1",height=buttonheight)
turnnumber.grid(row=8,column=6)
treebutton = tk.Button(window,text="Play\nComputer\nMove",height=buttonheight,command=lambda e=comp1:treep(e),bg='#F0F0F0')
treebutton.grid(row=9,column=2)
compfirstbutton = tk.Button(window,text="Computer\nPlays\nFirst",height=buttonheight,command=compfirst,bg='#F0F0F0')
compfirstbutton.grid(row=9,column=3)
compsecondbutton = tk.Button(window,text="Computer\nPlays\nSecond",height=buttonheight,command=compsecond,bg='#F0F0F0')
compsecondbutton.grid(row=9,column=4)
twoplayerbutton = tk.Button(window,text="2 Player\nGame",height=buttonheight,command=twoplayer,bg='#F0F0F0')
twoplayerbutton.grid(row=9,column=1)
self_playbutton = tk.Button(window,text="Computer\nSelf-play",height=buttonheight,command=self_play,bg='#F0F0F0')
self_playbutton.grid(row=9,column=5)
self_playframe = tk.Frame(window)
self_playframe.grid(row=10,column=5)
self_playlabel = tk.Label(self_playframe,text="No. of games")
self_playlabel.grid(row=0,column=0)
self_playentry = tk.Entry(self_playframe,width=buttonwidth)
self_playentry.grid(row=1,column=0)
resetbutton = tk.Button(window,text = "Reset",command=resetboard,bg='#F0F0F0')
beginbutton = tk.Button(window,text = "<<",command=tobegin,bg='#F0F0F0')
forwardmovebutton = tk.Button(window,text = "=>",command=forwardmove,bg='#F0F0F0')
backwardmovebutton = tk.Button(window,text = "<=",command=backwardmove,bg='#F0F0F0')
endbutton = tk.Button(window,text = ">>",command=toend,bg='#F0F0F0')
speedtoggleframe = tk.Frame(window)
speedtoggleframe.grid(row=9,column=6)
speedtogglelabel = tk.Label(speedtoggleframe,text = "Game Speed")
speedtogglelabel.grid(row=0,column=0)
speedtogglebutton = tk.Button(speedtoggleframe,text = "slow",command=switchgamespeed,bg='#F0F0F0')
speedtogglebutton.grid(row=1,column=0)
button_list = []
gameentryframe = tk.Frame(window)
gameentryframe.grid(row=10,column=0)
gameentrylabel = tk.Label(gameentryframe,text="Input String")
gameentrylabel.grid(row=0,column=0)
gameentryentry = tk.Entry(gameentryframe,width = int(buttonwidth*1.5))
gameentryentry.grid(row=1,column=0)
readgamebutton = tk.Button(window,text = "Read\nGame",command = readgame,bg='#F0F0F0')
readgamebutton.grid(row=9,column=0)
for i in range(7):
    button = tk.Button(window,width = buttonwidth, height = buttonheight, command = lambda e=i: place(e),pady = 5, padx = 5,bg = '#F0F0F0')  #These buttons are for the user to drop pieces.
    button.grid(row = 0,column = i)
    button_list.append(button)
label_list = []
for i in range(7):
    for j in range(6):
        label = tk.Label(window,image = imgs[2],borderwidth=0,bd=-10,padx=0,pady=0,highlightthickness=0) #These labels are the squares on the game board.
        label.grid(row = j + 1, column = i)
        label_list.append(label)
diagonals = [[(3,0),(4,1),(5,2),(6,3)],[(3,0),(2,1),(1,2),(0,3)],[(3,5),(4,4),(5,3),(6,2)],[(3,5),(2,4),(1,3),(0,2)],[(2,0),(3,1),(4,2),(5,3),(6,4)],
            [(4,0),(3,1),(2,2),(1,3),(0,4)],[(2,5),(3,4),(4,3),(5,2),(6,1)],[(4,5),(3,4),(2,3),(1,2),(0,1)],[(1,0),(2,1),(3,2),(4,3),(5,4),(6,5)],
             [(5,0),(4,1),(3,2),(2,3),(1,4),(0,5)],[(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)],[(6,0),(5,1),(4,2),(3,3),(2,4),(1,5)]] #list of every diagonal of length > 3.
window.title('Connect 4')
window.mainloop()


# In[ ]:





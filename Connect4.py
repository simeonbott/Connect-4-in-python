#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

#customizable variables. Note that tkinter measures buttonwidth/height in character lengths and pillow uses pixels to measure it's distances. This discrepancy
#means that you may need to customise the value of the ratio depending on your monitor.
circlewidth = 50
circleheight = 50
ratio = 25
buttonwidth = circlewidth*2//ratio
buttonheight = circleheight//ratio

#Switches who's turn it is and increases the turncount.
def switchturn():
    global turn
    global turncount
    turn = -(turn-1)
    turncount += 1
    playerturn.configure(bg = ['red','yellow'][turn])
    turnnumber.configure(text = "Turn " + str(turncount))

#checks whether a piece can be placed. If yes, place the piece and check if the player won, then switch to the next player's turn. If the board is full, end the game.
def place(i):
    global board
    height = 0
    for j in range(6):
        if 0 == board[i][j]:
            height += 1
    if height > 0:
        board[i][6 - height] = turn+1
        label_list[(i)*6 - 1 + height].configure(image=imgs[turn])
        if checkvictory((i,6 - height),turn):
            gameover(turn)
            return
        if 0 not in board:
            gameover(-1)
            return
        switchturn()

#Performs actions for after player wins, or in the case of a draw, and reveals the reset button.
def gameover(turn):
    winner = "winner!"
    if turn == -1:
        winner = " draw! "
    for i in range(7):
        button_list[i].configure(command = 'none',text = winner[i],bg = ['red','yellow','#F0F0F0'][turn])
        button_list[i].flash()
        button_list[i].configure(activebackground = ['red','yellow','#F0F0F0'][turn])
    resetbutton.grid(row=8,column=3)

#Resets the board to its beginning state, and hides the reset button.
def resetboard():
    global board
    global turncount
    resetbutton.grid_forget()
    for i in range(6):
        for j in range(7):
            label_list[j*6 + i].configure(image = imgs[2])
    for i in range(7):
        button_list[i].configure(bg = '#F0F0F0', activebackground = '#F0F0F0', command = lambda e=i: place(e), text = '')
    board = np.zeros(6*7).reshape(7,6)
    turnnumber.configure(text = "Turn 1")
    playerturn.configure(bg = 'yellow')
    turn = 1
    turncount = 1

#Given a line of values, checks if 4 are the turn players colour.
def check4inrow(vector,turn):        
    numinrow = 0
    for i in vector:
        if i == turn + 1:
            numinrow += 1
            if numinrow == 4:
                return True
        else:
            numinrow = 0
    return False

#Finds the rows and columns around the move played, and runs check4inrow to see if there are 4 in a row.
def checkvictory(move,turn):
    direction1 = board[move[0]]
    numinrow = 0
    if check4inrow(direction1,turn):
        return True
    direction2 = []
    for i in range(7):
        direction2.append(board[i,move[1]])
    if check4inrow(direction2,turn):
        return True
    direction3 = []
    for i in range(-5,6):
        if move[0] + i in range(7) and move[1] + i in range(6):
            direction3.append(board[move[0]+i,move[1]+i])
    if check4inrow(direction3,turn):
        return True
    direction4 = []
    for i in range(-5,6):
        if move[0] + i in range(7) and move[1] - i in range(6):
            direction4.append(board[move[0]+i,move[1]-i])
    if check4inrow(direction4,turn):
        return True
    return False
  
    
#setting up global variables.
board = np.zeros(6*7).reshape(7,6)
turn = 1
turncount = 1

#setting up piece images in pillow. Blue backgrounds form the board. A circle is of the desired colour is drawn ontop to create each state of the board.
window = tk.Tk() #A tkinter window must be present for ImageTk.PhotoImage.
im = Image.new('RGB', (circlewidth,circleheight), 'blue')
im2 = Image.new('RGB', (circlewidth,circleheight), 'blue')
im3 = Image.new('RGB', (circlewidth,circleheight),'blue')
draw = ImageDraw.Draw(im)
draw = draw.ellipse((circlewidth//10,circleheight//10,9*circlewidth//10,9*circleheight//10), fill = 'red', outline = 'red')
draw2 = ImageDraw.Draw(im2)
draw2 = draw2.ellipse((circlewidth//10,circleheight//10,9*circlewidth//10,9*circleheight//10), fill = 'yellow', outline = 'yellow')
draw3 = ImageDraw.Draw(im3)
draw3 = draw3.ellipse((circlewidth//10,circleheight//10,9*circlewidth//10,9*circleheight//10), fill = (240,240,240), outline = 'blue')
img = ImageTk.PhotoImage(im)
img2 = ImageTk.PhotoImage(im2)
img3 = ImageTk.PhotoImage(im3)
imgs = [img,img2,img3]
    
#setting up tkinter window and widgets.
playerturn = tk.Label(window, bg = 'yellow',height = buttonheight, width = buttonwidth)
playerturn.grid(row=8,column=0)
turnnumber = tk.Label(window,text = "Turn 1",height = buttonheight, width = buttonwidth)
turnnumber.grid(row=8,column=6)
resetbutton = tk.Button(window,text = "Reset",command = resetboard)
button_list = [] #The buttons lining the top row.
for i in range(7):
    button = tk.Button(window,width = buttonwidth, height = buttonheight, command = lambda e=i: place(e),pady = 5, padx = 5)
    button.grid(row = 0,column = i)
    button_list.append(button)
label_list = [] #These labels represent the game board.
for i in range(7):
    for j in range(6):
        label = tk.Label(window,image = imgs[2],borderwidth=0,bd=-10,padx=0,pady=0,highlightthickness=0)
        label.grid(row = j + 1, column = i)
        label_list.append(label)    
#running the tkinter window.
window.title('Connect 4')
window.mainloop()


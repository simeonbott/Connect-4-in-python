#!/usr/bin/env python
# coding: utf-8

# In[ ]:


columntypegames = [["2" for i in range(16)],['2' for i in range(16)],['2' for i in range(16)],['2' for i in range(16)]]
rowtypegames = [["2" for i in range(289)],['2' for i in range(289)],['2' for i in range(289)],['2' for i in range(289)],['2' for i in range(289)],['2' for i in range(289)]]
diagonaltypegames = [["2" for i in range(17)],['2' for i in range(17)],["2" for i in range(65)],['2' for i in range(65)],["2" for i in range(177)],['2' for i in range(177)]]
columntypescore = [["1" for i in range(16)],['1' for i in range(16)],['1' for i in range(16)],['1' for i in range(16)]]
rowtypescore = [["1" for i in range(289)],['1' for i in range(289)],['1' for i in range(289)],['1' for i in range(289)],['1' for i in range(289)],['1' for i in range(289)]]
diagonaltypescore = [["1" for i in range(17)],['1' for i in range(17)],["1" for i in range(65)],["1" for i in range(65)],["1" for i in range(177)],["1" for i in range(177)]]
for i in range(4):
    for j in range(16):
        if j in [4,9,14]:
            columntypescore[i][j] = '2'
        if j in [15]:
            columntypescore[i][j] = '0'
for i in range(6):
    for j in range(289):
        if j in [15, 30, 31, 47, 61, 62, 63, 79, 94, 95, 111, 127, 143, 158, 159, 175, 188, 189, 190, 191, 207, 223, 239, 254, 255, 271, 287]:
            rowtypescore[i][j] = '2'
        if j in [288]:
            rowtypescore[i][j] = '0'
for i in range(2):
    for j in range(17):
        if j in [15]:
            diagonaltypescore[i][j] = '2'
        if j in [16]:
            diagonaltypescore[i][j] = '0'
for i in range(2,4):
    for j in range(65):
        if j in [15, 30, 31, 47, 63]:
            diagonaltypescore[i][j] = '2'
        if j in [64]:
            diagonaltypescore[i][j] = '0'
for i in range(4,6):
    for j in range(177):
        if j in [15, 30, 31, 47, 60, 61, 62, 63, 79, 94, 95, 111, 126, 127, 143, 159, 175]:
            diagonaltypescore[i][j] = '2'
        if j in [176]:
            diagonaltypescore[i][j] = '0'
with open('connecttrainingvalues','w') as f:
    f.write("_".join(["-".join(i) for i in columntypegames]) + "¬" + "_".join(["-".join(i) for i in rowtypegames]) + "¬" + "_".join(["-".join(i) for i in diagonaltypegames])
            + "¬" + "_".join(["-".join(i) for i in columntypescore]) + "¬" + "_".join(["-".join(i) for i in rowtypescore]) + "¬" + "_".join(["-".join(i) for i in diagonaltypescore]))


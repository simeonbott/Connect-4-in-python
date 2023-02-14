#!/usr/bin/env python
# coding: utf-8

# In[ ]:


columntypegames = [["2" for i in range(16)],['2' for i in range(16)],['2' for i in range(16)],['2' for i in range(16)]]
rowtypegames = [["2" for i in range(289)],['2' for i in range(289)],['2' for i in range(289)],['2' for i in range(289)],['2' for i in range(289)],['2' for i in range(289)]]
diagonaltypegames = [["2" for i in range(17)],['2' for i in range(17)],["2" for i in range(65)],['2' for i in range(65)],["2" for i in range(177)],['2' for i in range(177)]]
columntypescore = [["1" for i in range(16)],['1' for i in range(16)],['1' for i in range(16)],['1' for i in range(16)]]
rowtypescore = [["1" for i in range(289)],['1' for i in range(289)],['1' for i in range(289)],['1' for i in range(289)],['1' for i in range(289)],['1' for i in range(289)]]
diagonaltypescore = [["1" for i in range(17)],['1' for i in range(17)],["1" for i in range(65)],["1" for i in range(65)],["1" for i in range(177)],["1" for i in range(177)]]
with open('connecttrainingvalues','w') as f:
    f.write("_".join(["-".join(i) for i in columntypegames]) + "¬" + "_".join(["-".join(i) for i in rowtypegames]) + "¬" + "_".join(["-".join(i) for i in diagonaltypegames])
            + "¬" + "_".join(["-".join(i) for i in columntypescore]) + "¬" + "_".join(["-".join(i) for i in rowtypescore]) + "¬" + "_".join(["-".join(i) for i in diagonaltypescore]))


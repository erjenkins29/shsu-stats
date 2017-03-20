
# ### Goal: 
# 
# Plot all possessions, extra graphics for turnovers, stalls, receiver errors, etc.
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


df = pd.read_csv("../SUIS-Wolves/Passes vs. YewWah Dogs 2017-03-11_09-15.csv")


point = np.unique(df.Point)

i=1
for pt in point:
    plt.subplot(len(point)/5 + 1,5,i)   ### will make a 5 column plot of possessions
    plt.plot(df.loc[df.Point==pt,"Start X (0 -> 1 = left sideline -> right sideline)"],df.loc[df.Point==pt,"Start Y (0 -> 1 = back of opponent endzone -> back of own endzone)"])
    plt.xticks([]);plt.yticks([])
    plt.xlim(0,1);plt.ylim(0,1)
    
    ## endzones
    normalized_line = 25. / (25+70+25)  ## normalized between 0 and 1, like the X-Y coordinates
    plt.plot([0,1],[normalized_line,normalized_line],'r')
    plt.plot([0,1],[1-normalized_line,1-normalized_line],'r')
    i+=1

plt.show()


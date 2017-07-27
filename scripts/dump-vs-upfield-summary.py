import pandas as pd
from numpy import round as rd

df = pd.read_csv("../WY-Wolves/Passes vs. YK-Buddha 2017-03-11_14-30.csv")
print("\nDump completion percentage:\n",rd(df.groupby(by="Thrower")["Dump?"].mean()*100,1).to_string())
print("\nDump attempts:\n",(df.groupby(by="Thrower")["Dump?"].count()).to_string())


import pandas as pd

df = pd.read_csv("../YW-Dogs/Passes vs. Suis 2017-03-24_16-10.csv")
huckthrows = df[df["Huck? (> 40m)"]==1]
print "\nHuck completion percentage:\n",((1 - huckthrows.groupby(by="Thrower")["Turnover?"].mean())*100).to_string()
print "\nHuck attempts:\n",(huckthrows.groupby(by="Thrower")["Turnover?"].count()).to_string()


#!/bin/bash

# for educational purposes/reference:  

# shell command for cutting the column header into a more readable form, then exporting to file.

head -n 1 "../YW-Dogs/Defensive Blocks vs. Suis 2017-03-24_16-10.csv" | sed s/,/"\n"/g

# if user wants to output to file, use ... 
# head -n 1 "../YW-Dogs/Defensive Blocks vs. Suis 2017-03-24_16-10.csv" | sed s/,/"\n"/g > ../doc/"Defensive blocks-columns.txt"

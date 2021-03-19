# -*- coding: utf-8 -*-
"""
@authors: Anna Christiane and Clarisse
"""

# This program...
# ...

# Run this program from the command line as
# $ python3 run.py

import qlearning
import sys

def writetofile(d1,d2):
    Qlearning_obj = qlearning.Qlearning(d1,d2)
    Qlearning_obj.getResult()

if __name__ == '__main__':
    try:
        d1 = sys.argv[1]
        d2 = sys.argv[2]
    except:
        print("TRY AGAIN!")
        d1 = 0
        d2 = 0
    writetofile(d1,d2)


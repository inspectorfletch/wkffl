import nflgame
import sys
import time
import datetime
from collections import OrderedDict
from openpyxl import load_workbook
from openpyxl.styles import colors
from openpyxl.styles import Font, Color
from openpyxl.styles import colors

import subprocess
    
if __name__ == '__main__':

    i = 0
    while True:
        print "Starting calculating: " + str(datetime.datetime.now())

        #if (i % 5 == 0):
        return_code = subprocess.call("python get_scores.py", shell=True)
        #else:
        #    return_code = subprocess.call("python get_scores.py -co", shell=True)

        print "Sleeping for 5 minutes: " + str(datetime.datetime.now())
        time.sleep(300)

#!/usr/bin/env python

#Reads in a *.VOL file from the extract directory
#Parses the year, month and day and then 
#places all files with the same day in a separate directory
#Justin Peter, USQ, ICACS
#04 June 2015

import os
import shutil

#input_dir = '/data/Q0128/pub/jpeter/radar/rapic/2009/extract/Marburg/'
#target_dir = '/data/Q0128/pub/jpeter/radar/rapic/2009/extract/Marburg/'

input_dir = '/data/Q0128/pub/jpeter/radar/rapic/2010/extract/Marburg/'
target_dir = '/data/Q0128/pub/jpeter/radar/rapic/2010/extract/Marburg/'

#input_dir = '/home/jpeter/justinp/python/suncorp/data/extract/qcif/'
#target_dir = '/home/jpeter/justinp/python/suncorp/data/extract/qcif/'
        
infiles = [file for file in os.listdir(input_dir) if file.endswith("VOL")]

infilepath = [input_dir+f for f in infiles]

for ifnm in range(0,len(infiles)):

    #Get the date information
    dstr = infiles[ifnm].split(".")
    date_string = dstr[2].split("_")[0]
    yyyy_str = date_string[0:4]
    mm_str   = date_string[4:6]
    dd_str   = date_string[6:8]

    #Make the target directory
    target_date_dir = os.path.join(target_dir, date_string)
    print target_date_dir

    #Check if the directory exists and make it if necessary
    if not os.path.exists(target_date_dir):
        os.mkdir(target_date_dir)

    #Move the file there
    shutil.move(infilepath[ifnm],target_date_dir)
    #shutil.copy(infilepath[ifnm],target_date_dir)


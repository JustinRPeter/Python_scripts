#!/usr/bin/env python

#Script to read the storms_to_tifs ascii files individually
#and merge them into a single file for a whole year
#Justin Peter
#USQ, ICACS
#19 March 2015

import os
from itertools import islice
import glob
#import csv
#import pandas as pd
#import numpy as np

#set the root data directory
#root_data_dir = '/data/Q0128/pub/jpeter/radar/rapic/titan/storms/'
#root_data_dir ='/media/jpeter/Elements/laptop/data/usq/titan/ho-nowcast-cawcr-a.bom.gov.au/nowcast/data/titan/titan/storms/NSW_Comp_35/output/'
root_data_dir = '/home/jpeter/justinp/rfiles/suncorp/data/titan/composite/'

#radar="Marburg"
#radar="MtStapl"
#refl_threshold =35
#refl_threshold =40
#refl_threshold =45
#refl_threshold =50

input_dir = root_data_dir

# See http://stackoverflow.com/questions/13051785/nested-list-comprehension-with-os-walk
# for explanation of the following line
#fls = [f for root,dirs,files in os.walk(root_data_dir) for f in files if f.endswith('tifs')]
trackfls = [os.path.join(root,f) for root,dirs,files in os.walk(root_data_dir) for f in files if f.endswith('tifs')]

# Now we need to extract the radar names
# First extract the base filenames
radar_name = [os.path.basename(f).split('_')[2] for f in trackfls]

# See
# http://www.cademuir.eu/blog/2011/10/20/python-searching-for-a-string-within-a-list-list-comprehension/
bloop=[m.group(1) for l in trackfls for m in [regex.search(l)] if m]



#Number of header lines
N=20
#for file in trackfls:

#output_dir='./'
#foutnm=output_dir+'all_storms_to_tif.out'
foutnm='all_storms_to_tif.out'
#fout=open(foutnm,'a')
#If the output file already exists remove it
try:
    os.remove(foutnm)
except OSError:
    pass
fout=open(foutnm,'a')

#for file in trackfls[:1]:
#for file in trackfls:
for file in fls:
#for file in trackfls[8:10]:
    fin=open(file,'r')

    lines=fin.readlines()
    lines_after_N=lines[N:]
    if len(lines) > N:
        fout.writelines(lines_after_N)
    fin.close()

fout.close()
 


#!/usr/bin/env python

#Script to read gather all the merged txt files output
#after merging all the storms_to_tifs files
#Justin Peter
#USQ, ICACS
#6 Aug 2015

import os
from itertools import islice

#set the root data directory
#root_data_dir = '/data/Q0128/pub/jpeter/radar/rapic/titan/storms/'
root_data_dir = '/home/jpeter/data/usq/titan/ho-nowcast-cawcr-a.bom.gov.au/nowcast/data/titan/titan/storms/'



radar = 'MtStapl'

refl_threshold = ['35','40','45']

# Now find all the files that concatenated files and copy them to a directory

comp_files = []
for rf in refl_threshold:
    cf = [os.path.join(root,f) \
                  for root,dirs,files in os.walk(root_data_dir+radar+'_'+rf) \
                  for f in files if f.endswith('txt')]
    comp_files.append(cf)

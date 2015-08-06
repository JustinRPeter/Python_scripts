#!/usr/bin/env python

import os
import subprocess

import glob

#set the root data directory
root_data_dir = '/data/Q0128/pub/jpeter/radar/rapic/titan/storms/'

radar="MtStapl"
#refl_threshold =35
#refl_threshold =40
#refl_threshold =45
refl_threshold =50

data_path=radar+'_'+str(refl_threshold)+'/'

input_dir = root_data_dir+data_path

fls = [f for f in os.listdir(input_dir) if f.endswith('th5')]
trackfls = [input_dir+f for f in fls]

for file in trackfls:
#for file in trackfls[:1]:
  outfile = "%s.txt" % file # a.th becomes tifs_a.th
  command = "storms_to_tifs -noparams -f %s  > %s " % (file, outfile) # create command
  #system(command) # Run command
  subprocess.call(command,shell=True) # Run command

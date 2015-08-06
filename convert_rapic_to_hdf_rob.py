#!/usr/bin/env python

#Reads all of the rapic files in a directory and processes
#them with rapic2ODIMH5 to create an hdf5 file
#Justin Peter, USQ, ICACS
#1 Mar 2015

import os

import glob

#using glob
#volfiles = glob.glob("/home/jpeter/justinp/python/suncorp/data/extract/*.VOL")

#using os
#input_dir = "/dm/scratch/radar/sam/radar/2000/output/vol/"
input_dir = "/home/jpeter/tmp_data/radar/rob/20111225/Gambier/extract/"
input_files=[f for f in os.listdir(input_dir) if f.endswith('VOL')]

output_dir = "/home/jpeter/tmp_data/radar/rob/20111225/Gambier/hdf/"

#for i in range(len(volfiles)):
for i in range(len(input_files)):
  outfile = output_dir+input_files[i]+".h5"
  command = "rapic2ODIMH5 " + input_dir+input_files[i] + " " +outfile
  os.system(command)
  

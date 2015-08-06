#!/usr/bin/env python

#Reads all of the rapic files in a directory and processes
#them with rapic2ODIMH5 to create an hdf5 file
#Justin Peter, USQ, ICACS
#24 Sep 2014

import os

import glob

#using glob
#volfiles = glob.glob("/dm/scratch/radar/sam/radar/2000/output/vol/*.VOL")
#volfiles = glob.glob("/dm/scratch/radar/sam/radar/2001/output/vol/*.VOL")
#volfiles = glob.glob("/home/jpeter/justinp/python/suncorp/data/extract/*.VOL")

#using os
#input_dir = "/dm/scratch/radar/sam/radar/2000/output/vol/"
#input_dir = "/dm/scratch/radar/sam/radar/2001/output/vol/"
#input_dir = "/home/jpeter/justinp/python/suncorp/data/extract/"
input_dir = "/home/jpeter/tmp_data/radar/rob/20111225/Gambier/extract/"
#input_files=os.listdir(input_dir)
input_files=[f for f in os.listdir(input_dir) if f.endswith('VOL')]
#input_files=glob.glob(input_dir+'*.VOL')

#output_dir = "/bm/gscratch/jpeter/radar/hdf/vol/2000/"
#output_dir = "/bm/gscratch/jpeter/radar/hdf/vol/2001/"
#output_dir = "/home/jpeter/justinp/python/suncorp/data/hdf/"
output_dir = "/home/jpeter/tmp_data/radar/rob/20111225/Gambier/hdf/"

#for file in input_files:
#for i in range(len(volfiles)):
for i in range(len(input_files)):
  #outfile = output_dir+file+".h5"
  #outfile = output_dir+input_files[i]+".h5"
  outfile = output_dir+input_files[i]+".h5"
  #command = "rapic2ODIMH5 " + input_dir+input_files[file] + " " +outfile
  command = "rapic2ODIMH5 " + input_dir+input_files[i] + " " +outfile
  #command = "rapic2ODIMH5 " + input_files[i] + " " +outfile
  #command = "rapic2ODIMH5 %s %s" % (file,outfile)
  os.system(command)
  

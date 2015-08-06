#!/usr/bin/env python

#Script to automate the Dsr2Vol and Rapic2Dsr processes
#Justin Peter, USQ, ICACS
#16 March 2015

import subprocess


#Set the radar names
# Set the radar names
#names=["Kanign", "Grafton", "Marburg", "MtStapl"]
names=["Kanign","Grafton","MtStapl"]

#Set the years we want to evaluate
years=[2000, 2001]

#Set the months
months=[01,02]
#months=[01,02,03,04,06,07,08,09,10,11,12]

#Set the days
days=[01,02,03,04,05]
#days=[01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,29,29,30,31]

TITAN_DIR="/home/ec2-user/titan"
PROJ_DIR=TITAN_DIR+"/projDir"
DATA_DIR="/data/Q0128/pub/jpeter/radar/rapic"
os.environ['TITAN_DIR']=TITAN_DIR
os.environ['PROJ_DIR']=PROJ_DIR
os.environ['DATA_DIR']=DATA_DIR

#Also see
#http://stackoverflow.com/questions/2231227/python-subprocess-popen-with-a-modified-environment
#os.environ(TITAN_DIR)="/home/ec2-user/titan"
#os.environ(PROJ_DIR)="$TITAN_DIR/projDir
##export DATA_DIR=$TITAN_DIR/titandata
#bash3=export DATA_DIR=/data/Q0128/pub/jpeter/radar/rapic

subprocess.call(bash1)


#import os

#import glob

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
  

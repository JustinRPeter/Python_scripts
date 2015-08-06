#!/usr/bin/env python

#Reads in a *.VOL file and extracts each rapic file
#Justin Peter, USQ, ICACS
#24 Sep 2014

import os
from itertools import islice

input_dir = '/home/jpeter/justinp/python/suncorp/data/raw/'
#fls = os.listdir(input_dir)
fls = ['radar.Cairns.20001218.VOL']

output_dir = '/home/jpeter/justinp/python/suncorp/data/extract/'

#fnm = 'radar.Cairns.20010102.VOL'

for fnm in fls:
    fin=open(input_dir+fnm,'r')
    #fin=open(fnm[fls],'r')
    
    lines=fin.readlines()
    num_lines=len(lines)
    n_tilts = int(lines[1].split()[1])
    #Number of lines to skip
    #3 lines before tilt information
    #(1)no_tilts (usually 15);(2)image_header end line;data;(3)image end
    #Gives total of 21 lines
    nskp = 3+n_tilts+1+1+1
    fin.close()
    
    #Extract each line containing the time
    hdr_info = lines[::nskp]
    #The length of this corresponds to the number of separate
    #rapic files in the VOL file
    n_sep_files = len(hdr_info)
    #Split the header. The last element (2) contains the time
    time_info = [i.split() for i in hdr_info]
    time_temp = [None]*n_sep_files
    time_hhmm = [None]*n_sep_files
    for i in range(len(time_info)):
        #time_temp[i] = int(time_info[i][2])
        time_temp[i] = time_info[i][2]
        time_hhmm[i] = time_temp[i][-4:]
    
    #We now have the time for every rapic file in the VOL file
    #Will append this to the file name to create the separate file names
    foutnm = [None]*n_sep_files
    indx   = fnm.find('.VOL')
    foutnm_pref = fnm[:indx]
    foutnm_suff = fnm[indx:] 
    #foutnm_pref = fnm[fls][:indx]
    #foutnm_suff = fnm[fls][indx:] 
    #Make the new file names
    for i in range(n_sep_files):
        #foutnm[i] = foutnm_pref+time_hhmm[i]+foutnm_suff 
        foutnm[i] = foutnm_pref+time_hhmm[i]+foutnm_suff 
        
    #Now extract out each slice and write to the files
    start = range(0,num_lines,nskp)
    stop  = [x+nskp for x in start]
    for i in range(n_sep_files):
        fin  = open(input_dir+fnm,'r')
        fout = open(output_dir+foutnm[i],"w")
        print foutnm[i], fout
        #fin = open(fnm,'r')
        #fin = open(fnm[fls],'r')
        #print i
        print start[i], stop[i]
        #fout=open(foutnm[i],"w")
        #print i
        fout.writelines(islice(fin, start[i], stop[i], 1))
        fout.close()
        fin.close()



#Work out the total number of lines in file.
#Be careful that we don't have empty lines.
#Shouldn't but if so refer to
#http://stackoverflow.com/questions/10673560/count-number-of-lines-in-a-txt-file-with-python-but-exclude-blank-lines

#Use simple way
#From http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
#num_lines = sum(1 for line in open('radar.Cairns.20010102.VOL'))
#num_lines = sum(1 for line in f.readlines())

#Get lines and assign some file information
##with open('radar.Cairns.20010102.VOL','r') as fin:
#with open(fnm,'r') as fin:
#    l1 = fin.readline()
#    l2 = fin.readline()

##The first line in the header gives the time and date information
#l1splt = l1.split()
#time_info = l1splt[range(len(l1splt))[-1]][-4:] 

##The second line gives how many tilts
##Usually 15 but will read in and pass as a variable
#l2splt = l2.split()
#n_tilts = int(l2splt[-1])

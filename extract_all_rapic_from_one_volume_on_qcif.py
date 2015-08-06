#!/usr/bin/env python

#Reads in a *.VOL file and extracts each rapic file
#Justin Peter, USQ, ICACS
#8 Oct 2014

import os
#import glob
import re
from itertools import islice
import paramiko #To connect to remote UQ cloud machine


#A function to evaluate the cumulative sum
#http://stackoverflow.com/questions/15889131/how-to-find-the-cumulative-sum-of-numbers-in-a-list
def accumu(lis):
    total = 0
    for x in lis:
        total += x
        yield total

#Connect to the remote UQ machine
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('q0078.qcloud.qcif.edu.au',username='Q0078-RW',password='Form1ica')

#input_dir = '/home/jpeter/justinp/python/suncorp/data/raw/'
#Look for files on UQ cloud machine
input_dir = '/data/Q0078/pub/jpeter/radar/rapic/2000/vol/'

#Open the ftp connection
sftp = client.open_sftp() 
fls = [f for f in sftp.listdir(input_dir) if f.endswith('.VOL')]
#fls = [f for f in os.listdir(input_dir) if f.endswith('.VOL')]

#output_dir = '/home/jpeter/justinp/python/suncorp/data/extract/'
output_dir = '/data/Q0078/pub/jpeter/radar/rapic/2000/extract/'

#fnm = 'radar.Cairns.20010102.VOL'
#fnm = 'radar.Kurnell.20000710.VOL'

#for fnm in fls[0:9]:
for fnm in fls:
    #fin=open(input_dir+fnm,'r')
    fin=sftp.open(input_dir+fnm,'r')
    #fin=open(fnm[fls],'r')
    
    lines=fin.readlines()
    fin.close()
    num_lines=len(lines)

    #Need to make number of tilts adaptive
    #n_tilts = int(lines[1].split()[1])
    #The following line returns the line with the appropriate string
    n_tilts_search = [x for x in lines if re.search("IMAGESCANS",x)]
    n_tilts = [int(i.split()[1]) for i in n_tilts_search]
    #The following line returns the indices
    n_tilts_indices = [i for i,x in enumerate(lines) if re.search("IMAGESCANS",x)]
    #Number of lines to skip
    #3 lines before tilt information
    #(1)no_tilts (usually 15);(2)image_header end line;data;(3)image end
    #Gives total of 21 lines
    #nskp = 3+n_tilts+1+1+1
    nskp = [3+x+1+1+1 for x in n_tilts]
    nskp.insert(0,0) #Insert 0 to get first line
    #nskp.pop()       #Remove last element as this goes past IMAGEHEADER
    nskp_cumsum = list(accumu(nskp))
#   fin.close()
    
    #Extract each line containing the time
    #hdr_info = lines[::nskp]
    #hdr_info = [lines[i] for i in nskp_cumsum]
    hdr_info = [lines[i] for i in nskp_cumsum[0:-1]]
    #The length of this corresponds to the number of separate
    #rapic files in the VOL file
    n_sep_files = len(hdr_info)
    #Split the header. The last element (2) contains the time
    time_info = [i.split() for i in hdr_info]
#    time_temp = [None]*n_sep_files
#    time_hhmm = [None]*n_sep_files
#    for i in range(len(time_info)):
#        #time_temp[i] = int(time_info[i][2])
#        time_temp[i] = time_info[i][2]
#        time_hhmm[i] = time_temp[i][-4:]
    time_extract = [time_info[i][2] for i in range(n_sep_files)]
    time_hhmm = [time_extract[i][-4:] for i in range(n_sep_files)]
    
    #We now have the time for every rapic file in the VOL file
    #Will append this to the file name to create the separate file names
    #foutnm = [None]*n_sep_files
    indx   = fnm.find('.VOL')
    foutnm_pref = fnm[:indx]
    foutnm_suff = fnm[indx:] 
    #Make the new file names
#   for i in range(n_sep_files):
#       #foutnm[i] = foutnm_pref+time_hhmm[i]+foutnm_suff 
#       foutnm[i] = foutnm_pref+time_hhmm[i]+foutnm_suff 
    foutnm=[foutnm_pref+time_hhmm[i]+foutnm_suff for i in range(n_sep_files)]
        
    #Now extract out each slice and write to the files
    #start = range(0,num_lines,nskp)
    #stop  = [x+nskp for x in start]
    start = nskp_cumsum[0:-1] 
    #stop  = nskp_cumsum[1:]
    stop  = nskp_cumsum[1:]
    #stop.append(nskp_cumsum[-1]+nskp[-1])
    for i in range(n_sep_files):
        fin  = sftp.open(input_dir+fnm,'r')
        fout = sftp.open(output_dir+foutnm[i],"w")
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

#!/usr/bin/env python

#Reads in a *.VOL file and extracts each rapic file
#Justin Peter, USQ, ICACS
#This version will read files from flurry and write them to ACIF
#16 Oct 2014

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

#Connect to qcif
in_client = paramiko.SSHClient()
in_client.load_system_host_keys()
in_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
in_client.connect('q0078.qcloud.qcif.edu.au',username='Q0078-RW',password='Form1ica')

#Connect to the remote UQ machine
out_client = paramiko.SSHClient()
out_client.load_system_host_keys()
out_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
out_client.connect('q0078.qcloud.qcif.edu.au',username='Q0078-RW',password='Form1ica')

#Look for files on QCIF
input_dir = '/data/Q0078/pub/jpeter/radar/rapic/2012/vol/'

#Open the ftp connections
#First to flurry
in_sftp = in_client.open_sftp() 
fls = [f for f in in_sftp.listdir(input_dir) if f.endswith('.VOL')]
#fls = [f for f in os.listdir(input_dir) if f.endswith('.VOL')]
#Then to QCIF
out_sftp = out_client.open_sftp()

#output_dir = '/home/jpeter/justinp/python/suncorp/data/extract/'
output_dir = '/data/Q0078/pub/jpeter/radar/rapic/2012/extract/'

#for fnm in fls[0:1]:
for fnm in fls:
    #fin=open(input_dir+fnm,'r')
    #with in_sftp.open(input_dir+fnm,'r') as fin:
    #try:
        #fin=in_sftp.open(input_dir+fnm,'r')
    with in_sftp.open(input_dir+fnm,'r') as fin:
    #fin=open(fnm[fls],'r')
    
        lines=fin.readlines()
    #finally:
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
#       fin.close()
        
        #Extract each line containing the time
        #hdr_info = lines[::nskp]
        #hdr_info = [lines[i] for i in nskp_cumsum]
        hdr_info = [lines[i] for i in nskp_cumsum[0:-1]]
        #The length of this corresponds to the number of separate
        #rapic files in the VOL file
        n_sep_files = len(hdr_info)
        #Split the header. The last element (2) contains the time
        time_info = [i.split() for i in hdr_info]
        time_extract = [time_info[i][2] for i in range(n_sep_files)]
        time_hhmm = [time_extract[i][-4:] for i in range(n_sep_files)]
        
        #We now have the time for every rapic file in the VOL file
        #Will append this to the file name to create the separate file names
        #foutnm = [None]*n_sep_files
        indx   = fnm.find('.VOL')
        foutnm_pref = fnm[:indx]
        foutnm_suff = fnm[indx:] 
        #Make the new file names
        foutnm=[foutnm_pref+time_hhmm[i]+foutnm_suff for i in range(n_sep_files)]
            
        #Now extract out each slice and write to the files
        start = nskp_cumsum[0:-1] 
        stop  = nskp_cumsum[1:]

    with in_sftp.open(input_dir+fnm,'r') as fin:
        #try:
            for i in range(n_sep_files):
            #fin  = in_sftp.open(input_dir+fnm,'r')
                #fout = out_sftp.open(output_dir+foutnm[i],"w")
                with out_sftp.open(output_dir+foutnm[i],"w") as fout:
                    print foutnm[i], fout
        #fin = open(fnm,'r')
        #fin = open(fnm[fls],'r')
        #print i
                    print start[i], stop[i]
        #fout=open(foutnm[i],"w")
        #print i
                    fout.writelines(islice(fin, start[i], stop[i], 1))
                    fin.flush()
                    #fout.close()
        #finally:        
            #fin.close()

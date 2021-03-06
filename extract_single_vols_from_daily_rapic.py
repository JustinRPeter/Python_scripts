#!/usr/bin/env python

#Reads in a *.VOL file and extracts each rapic file
#Justin Peter, USQ, ICACS
#24 Feb 2015

import os
import re
from itertools import islice

#A function to evaluate the cumulative sum
#http://stackoverflow.com/questions/15889131/how-to-find-the-cumulative-sum-of-numbers-in-a-list
def accumu(lis):
    total = 0
    for x in lis:
        total += x
        yield total

#input_dir = '/home/jpeter/tmp_data/radar/rob/20111225/NE_Vic/rapic/'
input_dir = '/data/Q0128/pub/jpeter/radar/rapic/2005/vol/'

fls = [f for f in os.listdir(input_dir) if f.endswith('.VOL')]
##fls = [f for f in os.listdir(input_dir) if f.endswith('.VOL1')]
#fls = ['radar.Kurnell.20010312.VOL']

#output_dir = '/home/jpeter/justinp/python/suncorp/data/extract/'
#output_dir = '/home/jpeter/tmp_data/radar/rob/20111225/Bnsdale/extract/'
#output_dir = '/home/jpeter/tmp_data/radar/rob/20111225/Gambier/extract/'
#output_dir = '/home/jpeter/tmp_data/radar/rob/20111225/NE_Vic/extract/'
output_dir = '/data/Q0128/pub/jpeter/radar/rapic/2005/extract/'

#fnm = 'radar.Cairns.20010102.VOL'
#fnm = 'radar.Kurnell.20000710.VOL'

for fnm in fls:
    fin=open(input_dir+fnm,'r')
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
    nskp_cumsum = list(accumu(nskp))
    
    #Extract each line containing the time
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
    indx   = fnm.find('.VOL')
    foutnm_pref = fnm[:indx]
    foutnm_suff = fnm[indx:] 
    #Make the new file names
    foutnm=[foutnm_pref+time_hhmm[i]+foutnm_suff for i in range(n_sep_files)]
        
    #Now extract out each slice and write to the files
    start = nskp_cumsum[0:-1] 
    stop  = nskp_cumsum[1:]
    for i in range(n_sep_files):
        fin  = open(input_dir+fnm,'r')
        fout = open(output_dir+foutnm[i],"w")
        print foutnm[i], fout
        print start[i], stop[i]
        fout.writelines(islice(fin, start[i], stop[i], 1))
        fout.close()
        fin.close()

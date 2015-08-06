#!/usr/bin/env python

#Script to read the storms_to_tifs ascii files individually
#and merge them into a single file for a whole year
#Justin Peter
#USQ, ICACS
#19 March 2015

import os
from itertools import islice
#import csv
#import pandas as pd
#import numpy as np

#set the root data directory
#root_data_dir = '/data/Q0128/pub/jpeter/radar/rapic/titan/storms/'
root_data_dir = '/home/jpeter/data/usq/titan/ho-nowcast-cawcr-a.bom.gov.au/nowcast/data/titan/titan/storms/'

#radar="Marburg"
radar = 'MtStapl'

refl_threshold = ['35','40','45']
#refl_threshold = '35'
#refl_threshold = '40'
#refl_threshold = '45'
#refl_threshold = '50'

#yyyy = '2011'
yyyy = ['2011','2012','2013','2014','2015']

for yr in yyyy:
    for rf in refl_threshold:
        #data_path=radar+'_'+str(refl_threshold)+'/'
        data_path=radar+'_'+str(rf)+'/'
        
        #input_dir = root_data_dir+data_path+'output/'+yyyy+'/'
        input_dir = root_data_dir+data_path+'output/'+yr+'/'
        
        #fls = [f for f in os.listdir(input_dir) if f.endswith('txt')]
        #trackfls = [input_dir+f for f in fls]
        
        trackfls = [os.path.join(root,f) for root,dirs,files in os.walk(input_dir) for f in files if f.endswith('tifs')]
        
        
        #Number of header lines
        N=20
        #for file in trackfls:
        
        output_dir=input_dir
        #foutnm=output_dir+'all_storms_to_tif.out'
        #foutnm=output_dir+radar+'_'+yyyy+'_'+refl_threshold+'.txt'
        #foutnm=output_dir+radar+'_'+yyyy+'_'+rf+'.txt'
        foutnm=output_dir+radar+'_'+yr+'_'+rf+'.txt'
        #fout=open(foutnm,'a')
        #If the output file already exists remove it
        try:
            os.remove(foutnm)
        except OSError:
            pass
        fout=open(foutnm,'a')
        
        #for file in trackfls[:1]:
        for file in trackfls:
        #for file in trackfls[8:10]:
            fin=open(file,'r')
        
            lines=fin.readlines()
            lines_after_N=lines[N:]
            if len(lines) > N:
                fout.writelines(lines_after_N)
            fin.close()
        
        fout.close()
 


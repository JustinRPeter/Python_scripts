#!/usr/bin/env python

#Reads in a *.VOL file and extracts each rapic file
#Ananda Maiti, USQ, ICACS
#18 Mar 2015

import os
import sys
import time

#set the input/output paramters
#output_dir = 'G:\\extract\\'
#input_dir = 'G:\\'
#output_dir = '/data/Q0128/pub/jpeter/radar/rapic/2000/extract/'
#input_dir = '/data/Q0128/pub/jpeter/radar/rapic/2000/vol/'
#output_dir = '/data/Q0128/pub/jpeter/radar/rapic/2009/extract/Marburg/'
#input_dir = '/data/Q0128/pub/jpeter/radar/rapic/2009/vol/Marburg/'
output_dir = '/data/Q0128/pub/jpeter/radar/rapic/2010/extract/Marburg/'
input_dir = '/data/Q0128/pub/jpeter/radar/rapic/2010/vol/Marburg/'
lines = []

#prepare list of files
fls = [f for f in os.listdir(input_dir) if f.endswith('.VOL')]

#this is the list of keywords to look for. The assumption is that
#they will appear in this exact sequence without any blank lines in
#between them
list_key = ['/IMAGE:', '/IMAGESCANS:', '/IMAGESIZE:']

#given a line at 'pointnow', this finds if the 'key' is there in any of
#the previous 3 lines
def find_key(key, pointnow):

    r = False

    startlookingat = (pointnow - 3)
    if (pointnow - 3 < 0):
        startlookingat = 0

    for local_line in lines[startlookingat:(pointnow)]:
        if (local_line.startswith('/')):
            if(local_line.startswith(key)):
                r = True
        elif (key in local_line):
            r = True

    return r

#given a poosition of the current line, this returns upto 3 lines before
#the current line containing the keywords
def getlastpoint(pointnow):

    #print (len(list_key))
    r = 0
    found_keys = {}

    for key in list_key:
        found_keys[key] = False
        
    for key in list_key:
        #print 'Looking for ', key
        found_keys[key] = find_key(key, pointnow)

    level = 0

    if (found_keys['/IMAGESIZE:']):
        level = level + 1
    if (found_keys['/IMAGESCANS:']):
        level = level + 1
    if (found_keys['/IMAGE:']):
        level = level + 1

    if (level == 0):
        r = -1
    else:
        r = pointnow - level
    
    return r

#checks if the line contains '/SCAN     1:'. This is the pivot for pushing backwards
def thisistheline(strline):
    r = False
    if(strline.startswith('/SCAN    1:')):
            r = True
    else:
        if(strline.startswith('/SCAN')):
            for i in range(5, len(strline) - 3):
                if (strline[i:].startswith(' 1:')):
                    r = True
                    break;
    return r

#removes any of the keywords attached at the end of the line
def processed(strline):
    r = strline
    for key in list_key:
        if(key in strline):
            if(strline.find(key) >= 1):
                r = strline[0:strline.find(key)]
            else:
                r = ''
            break
    return r


#fls = ['radar.Kurnell.20010312.VOL']

#The main file to record the metadata
filecatalog = open(output_dir + 'catalog.txt', 'w')

#traverse through the list of files
for fnm in fls:

    try:
        #A number to mark all files uniquely
        counter = 100000;
        #read from file
        fin=open(input_dir + fnm, 'r')    
        lines=fin.readlines()
        fin.close()

        #fout points to the current sub-file. It is initially opened with
        #junk file to make it global
        fout = open(output_dir + 'test.txt', 'w')

        #count the line number in the current file
        linecounter = 0

        #traverse through each line for the current file
        for line in lines:
            #if this line contans '/SCAN'
            if (thisistheline(line)):
                #close ay previous sub-file
                fout.close();

                fname = fnm[:-4]

                #find the numebr of lines to go back
                startingpos = getlastpoint(linecounter)
                print str(startingpos) + ' ' + str(linecounter)
                #time.sleep(5)

                #check if any key containing number of lines were found before '/SCAN'
                if(startingpos >= 0):
                    #create empty array
                    _templines = [None] * (linecounter - startingpos)

                    #the id of a subfile - with the time of the day information
                    timeid_ = 'UDFN'

                    #gather all the previous lines in to array
                    for localcounter in range(startingpos, linecounter):
                        x = lines[localcounter]
                        #start to gather any line only from the position where the keyword starts
                        _templines[localcounter - startingpos] = x[x.find('/IMAGE'):]
                        #if the /IMAGE: is avaiable then get the subfile number
                        if(_templines[localcounter - startingpos].startswith('/IMAGE:')):
                           timeid_ = _templines[localcounter - startingpos].split(' ')[2].strip(' \n');
                           
                    #open new sub-file
                    fout = open(output_dir + fname + '_' + timeid_ + '_' + str(counter) + '.VOL', 'w')
                    print 'Got our start for ', fname + ' ' + timeid_
                    #record metadata
                    filecatalog.write('Got our start for ' + fname + ' ' + timeid_ + ' ' + str(counter) + ' at line ' + str(startingpos) + '\n')
                    #write all the previous lines into the newly opened file
                    for _templine in _templines:
                        fout.write(_templine)                
                else:
                    #if no keyword is found before the /SCAN
                    print 'Got our start for ', fname + ' UDF'
                    filecatalog.write('Got our start for ' + fname + ' UDF at line ' + str(startingpos) + '\tThere is Problem with this file\n')
                    #open new subfile with 'UDF'
                    fout = open(output_dir + fname + '_' + 'UDF' + '_' + str(counter) + '.VOL', 'w')
            
                filecatalog.flush()
                #increase counter
                counter = counter + 1
                
            #print line

            #do not write any of the lines starting with the keywords as they are already aritten in the beginning
            #otherwise write the current line from which any of the keyword is removed
            if(not(line.startswith('/IMAGE:') or line.startswith('/IMAGESCANS:') or line.startswith('/IMAGESIZE:'))):
                fout.write(processed(line))
                fout.flush()

            #increase linecounter
            linecounter = linecounter + 1
            #time.sleep(0.001)    
                    
        print len(lines)
        # record metadata about the number of lines in the file
        filecatalog.write('Total Lines in ' + fname + ' : ' + str(len(lines)) + '\n')
        filecatalog.flush()

    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        filecatalog.write('File Error in ' + fnm + "I/O error({0}): {1}".format(e.errno, e.strerror) + '\n')
        filecatalog.flush()
    except ValueError:
        print "Could not convert data to an integer."
        filecatalog.write('Execution Error in ' + fnm + '\n')
        filecatalog.flush()
    except:
        print "Unexpected error:", sys.exc_info()[0]
        filecatalog.write('Unknown Error in ' + fnm + "Unexpected error:", sys.exc_info()[0] + '\n')
        filecatalog.flush()

filecatalog.close()
#XXX = raw_input('XXX')

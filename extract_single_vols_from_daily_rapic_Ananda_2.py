#!/usr/bin/env python

#Reads in a *.VOL file and extracts each rapic file
#Ananda Maiti, USQ, ICACS
#18 Mar 2015

import os
import sys
import time

#set the input/output paramters
#output_dir = 'E:\\NOT Bakwas\\extract\\'
#input_dir = 'G:\\'
#output_dir = '/data/Q0128/pub/jpeter/radar/rapic/2005/extract/'
#input_dir = '/data/Q0128/pub/jpeter/radar/rapic/2005/vol/Marburg/'
output_dir = '/data/Q0128/pub/jpeter/radar/rapic/2009/extract/Marburg/'
input_dir = '/data/Q0128/pub/jpeter/radar/rapic/2009/vol/Marburg/'
lines = []
list_of_files = []
incomplete_ = False

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
def processed(strline, eparms):
    r = strline
    for key in list_key:
        if(key in strline):
            if(strline.find(key) >= 1):
                r = strline[0:strline.find(key)]
                r = r + 'END RADAR IMAGE\n/IMAGEEND: ' + eparms
                global incomplete_
                incomplete_ =  True
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

        list_of_files = []
        
        #fout points to the current sub-file. It is initially opened with
        #junk file to make it global
        fout = open(output_dir + 'test.txt', 'w')

        #count the line number in the current file
        linecounter = 0

        scan_checks = -9

        curr_name = ''

        no_scans = -9
        #traverse through each line for the current file
        for line in lines:
            #if this line contans '/SCAN 1'
            if (thisistheline(line)):                

                #print incomplete_
                if(not(no_scans == scan_checks)):
                    filecatalog.write('*********This file had the SCAN discrepancy Expected -' + str(no_scans) + ' Found -' + str(scan_checks) + '\n')
                    filecatalog.flush()
                    fout.close()

                    if(incomplete_):
                        filecatalog.write('*********This file had the Incomplete Ending \n')
                        if(os.path.isfile(curr_fname + '_FI.VOL')):
                            os.remove(curr_fname + '_FI.VOL')
                        os.rename(curr_fname + '.VOL', curr_fname + '_FI.VOL')
                    else:
                        if(os.path.isfile(curr_fname + '_F.VOL')):
                           os.remove(curr_fname + '_F.VOL')
                        os.rename(curr_fname + '.VOL', curr_fname + '_F.VOL')
                else:
                    #close ay previous sub-file
                    fout.close()

                    if(incomplete_):
                        filecatalog.write('*********This file had the Incomplete Ending \n')
                        if(os.path.isfile(curr_fname + '_I.VOL')):
                           os.remove(curr_fname + '_I.VOL')
                        os.rename(curr_fname + '.VOL', curr_fname + '_I.VOL')

                #global incomplete_
                incomplete_ = False

                fname = fnm[:-4]
                timeid_ = ''
                other_id = ''
                
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

                    no_scans = -3
                    scan_checks = 0
                    
                    #gather all the previous lines in to array
                    for localcounter in range(startingpos, linecounter):
                        x = lines[localcounter]
                        #start to gather any line only from the position where the keyword starts
                        _templines[localcounter - startingpos] = x[x.find('/IMAGE'):]
                        #if the /IMAGE: is avaiable then get the subfile number
                        if(_templines[localcounter - startingpos].startswith('/IMAGE:')):
                           timeid_ = _templines[localcounter - startingpos].split(' ')[2].strip(' \n')
                           other_id = _templines[localcounter - startingpos].split(' ')[1].strip(' \n')

                        if(_templines[localcounter - startingpos].startswith('/IMAGESCANS:')):
                           no_scans = int(_templines[localcounter - startingpos].split(' ')[1].strip(' \n'))
                           
                           
                    #open new sub-file
                    if(not((fname + '_' + timeid_) in list_of_files)):
                        fout = open(output_dir + fname + '_' + timeid_ + '_' + str(counter) + '.VOL', 'w')
                        curr_fname = output_dir + fname + '_' + timeid_ + '_' + str(counter)

                        print 'Got our start for ', fname + ' ' + timeid_
                        #record metadata
                        filecatalog.write('Got our start for ' + fname + ' ' + timeid_ + ' ' + str(counter) + ' at line ' + str(startingpos) + '\n')
                    else:
                        fout = open(output_dir + 'DUP' + str(list_of_files.count(fname + '_' + timeid_)) + fname + '_' + timeid_ + '_' + str(counter) + '.VOL', 'w')
                        curr_fname = output_dir + 'DUP' + str(list_of_files.count(fname + '_' + timeid_)) + fname + '_' + timeid_ + '_' + str(counter)
                        
                        print 'Got our start for ', fname + ' ' + timeid_
                        #record metadata (dup)
                        filecatalog.write('Got our start for (Duplicate)\t' + fname + ' ' + timeid_ + ' ' + str(counter) + ' at line ' + str(startingpos) + '\n')


                    list_of_files.append(fname + '_' + timeid_)

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
                fout.write(processed(line, other_id + ' ' + timeid_))
                fout.flush()

            if(line.startswith('/SCAN')):
                scan_checks = scan_checks + 1
                
            #increase linecounter
            linecounter = linecounter + 1
            #time.sleep(0.001)    
                    
        print len(lines)
        # record metadata about the number of lines in the file
        filecatalog.write('Total Lines in ' + fname + ' : ' + str(len(lines)) + '\n\n\n')
        filecatalog.flush()

        fout.flush()
        fout.close()
        
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        filecatalog.write('File Error in ' + fnm + "I/O error({0}): {1}".format(e.errno, e.strerror) + '\n')
        filecatalog.flush()
    except ValueError:
        print "Could not convert data to an integer."
        filecatalog.write('Execution Error in ' + fnm + '\n')
        filecatalog.flush()
    except:
        print "Unexpected error:", str(sys.exc_info()[0]), str(sys.exc_info()[1]), str(sys.exc_info()[2])
        filecatalog.write('Unknown Error in ' + fnm + "Unexpected error:" + str(sys.exc_info()[0]) + '\n' + str(sys.exc_info()[1]) + '\n')
        filecatalog.flush()

filecatalog.close()
XXX = raw_input('XXX')

#!/usr/bin/env python
#
# Routines related generating reports from text file generated by fiwalk
# 

import re
import os
from bc_utils import is_comment_line
from bc_utils import get_file_info
from bc_utils import fw_get_image_info

#
# This function makes a dictionary datastructure of the contents of
# of the input file, which has the file attributes for every file found.
# We will make an array of dictionaries. Each dictionary is a set of the 
# attributes for each file. The List myDictArrayList has the dictionary as 
# each of its element. So it is essentially a 2-dimentional array.
# Number of elements in each dictonary is the number of attributes for each 
# file from the fiwalk output. The number of elements in the big array 
# myDictArrayList is the number of files in the fiwalk output file.
#
def make_dict(linenum, line, image_fileinfo, image_info, FiwalkReport):
    if not line.strip():
        ## EMPTY LINE
        return
    line1 = re.split(":", line)
    if 'md5' in line1[0] or 'sha1' in line1[0]:
        ## print("D:make_dict: SKIPPING MD5 and SHA1: line1:", line1[0])
        return
    if line1[0] in image_fileinfo:
        fw_get_image_info(line1, image_info) 
        return

    # If the line has "filename", it is the beginning of a new array element
    # We will append the previous element to the dictionary. But if this is
    # the very first array element, there is nothing to append. So the flag
    # "is_first_file" is used which is toggeld here to indicate the subsequent
    # one is not the first element.
    #
    if line1[0] in 'filename': #Next sub-array 
        FiwalkReport.array_ind = FiwalkReport.array_ind + 1
        if FiwalkReport.is_first_file==True:
            FiwalkReport.is_first_file = False
        else:
            ## print("D: make_dict: NOT first file anymore is_first_file flag is false ")
            ## for j in range(0, len(FiwalkReport.dict_array)):
                ## print(FiwalkReport.dict_array[j])
            ## print("DEBUG: Last element: ARRAY INDEX NOW IS: ", line1[0], FiwalkReport.array_ind)
            # last element added. Append the array to the dict.
            FiwalkReport.fiDictList.append({FiwalkReport.dict_array[0]:FiwalkReport.dict_val[0], \
                         FiwalkReport.dict_array[1]:FiwalkReport.dict_val[1],\
                         FiwalkReport.dict_array[2]:FiwalkReport.dict_val[2],\
                         FiwalkReport.dict_array[3]:FiwalkReport.dict_val[3],\
                         FiwalkReport.dict_array[4]:FiwalkReport.dict_val[4],\
                         FiwalkReport.dict_array[5]:FiwalkReport.dict_val[5],\
                         FiwalkReport.dict_array[6]:FiwalkReport.dict_val[6],\
                         FiwalkReport.dict_array[7]:FiwalkReport.dict_val[7],\
                         FiwalkReport.dict_array[8]:FiwalkReport.dict_val[8],\
                         FiwalkReport.dict_array[9]:FiwalkReport.dict_val[9],\
                         FiwalkReport.dict_array[10]:FiwalkReport.dict_val[10],\
                         FiwalkReport.dict_array[11]:FiwalkReport.dict_val[11],\
                         FiwalkReport.dict_array[12]:FiwalkReport.dict_val[12],\
                         FiwalkReport.dict_array[13]:FiwalkReport.dict_val[13],\
                         FiwalkReport.dict_array[14]:FiwalkReport.dict_val[14],\
                         FiwalkReport.dict_array[15]:FiwalkReport.dict_val[15],\
                         FiwalkReport.dict_array[16]:FiwalkReport.dict_val[16],\
                         FiwalkReport.dict_array[17]:FiwalkReport.dict_val[17],\
                         FiwalkReport.dict_array[18]:FiwalkReport.dict_val[18],\
                         FiwalkReport.dict_array[19]:FiwalkReport.dict_val[19],\
                         FiwalkReport.dict_array[20]:FiwalkReport.dict_val[20],\
                         FiwalkReport.dict_array[21]:FiwalkReport.dict_val[21],\
                         FiwalkReport.dict_array[22]:FiwalkReport.dict_val[22]})

    for ind in range (0, (len(FiwalkReport.dict_array)-1)):
        if line1[0] in FiwalkReport.dict_array[ind]:
            ## print("D: make_dict: Adding line1[0], ind: ", line1[0], line1[1].rstrip(), ind) 
            ## print("D: make_dict: INDEX", FiwalkReport.array_ind, line1[0])

            # Either alloc or unalloc will be present for any file. So set the
            # the value of the other one to 0, for future reference.
            if line1[0] in 'alloc':
                FiwalkReport.dict_val[6] = 0     
            elif line1[0] in 'unalloc':
                FiwalkReport.dict_val[5] = 0     

            FiwalkReport.dict_val[ind] = line1[1].rstrip() 
            break

#
# Read in the lines from the fiwalk generated text file, populate the
# array of dictionaries, fiDictList, and geenrate fiwalk-based reports 
#
def bc_process_textfile(fn, image_fileinfo, image_info, FiwalkReport):
    ifd = open(fn.fiwalk_txtfile, "r")
    linenum = 0
    for line in ifd:
        linenum = linenum + 1
        if is_comment_line(line):
            continue # eliminate comments

        # Add the info to the dictionary
        make_dict(linenum, line, image_fileinfo, image_info, FiwalkReport)

        # First, form the Dictionary of formats found in this fiwalk output file.
        get_file_info(line, FiwalkReport)

    # Write collected statistics to output file
    FiwalkReport.bc_generate_fiwalk_reports(FiwalkReport, fn)

'''
    ## Note: The following will be uncommented when the text reports
    ## are fully implemented.
    of1.write(b'Input File Name: ')
    #of.write(str(input_file))
    of1.write(bytes(input_file, 'UTF-8')) 
    of1.write(b'\n\n')
    of1.write(b'\nTotal Files:\t\t')
    of1.write(bytes(str(self.numfiles), 'UTF-8'))
    of1.write(b'\nTotal Directories:\t')
    of1.write(bytes(str(self.dirs), 'UTF-8'))
    of1.write(b'\nTotal Deleted Files:\t')
    of1.write(bytes(str(self.deleted_files), 'UTF-8'))
    of1.write(b'\nTotal Unused Files:\t')
    of1.write(bytes(str(self.unused_files), 'UTF-8'))
    of1.write(b'\nFiles with nliks > 1:\t')
    of1.write(bytes(str(self.moreNumlinks), 'UTF-8'))
    of1.write(b'\nEmpty Files:\t\t')
    of1.write(bytes(str(self.emptyFiles), 'UTF-8'))
    of1.write(b'\nBig Files : \t')
    of1.write(bytes(str(self.bigFiles), 'UTF-8'))
    of1.write(b'\n\n')

    write_file_details(of)

    of.close()
    of1.close()
    of2.close()
'''



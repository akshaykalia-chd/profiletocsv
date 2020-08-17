#!/usr/bin/python
import os
from datetime import datetime

def prep_stat_file(myfiles, counter_list):
    for myfile in myfiles:
        if ("-profiler-" in myfile and (".csv" in myfile)):
            print datetime.now(), 'Found', myfile
            profiler_file = open(myfile, 'r')
            lines = profiler_file.readlines()
            for counter in counter_list:
                outfile = counter + ".csv"
                try:
                    open_outfile = open(outfile, 'a')
                except IOError:
                    continue
                for line in lines:
                    if counter in line:
                        open_outfile.write(line)
                open_outfile.close()
            print datetime.now(), 'Done processing', myfile
            profiler_file.close()

def profile_to_csv(myfiles):
    for myfile in myfiles:
        if ("-profiler-" in myfile and not (".csv" in myfile)):
            outfile = myfile.split(".")
            outfile = outfile[0] + ".csv"
            open(outfile, 'w')
            open_outfile = open(outfile, 'a')
            print datetime.now(), 'Found', myfile
            print datetime.now(), 'Converting', myfile, 'to CSV'
            profiler_file = open(myfile, 'r')
            lines = profiler_file.readlines()
            time_stamp = ""
            for line in lines:
                if "sub=App]" in line:
                    time_stamp = line.split()
                    time_stamp = time_stamp[0]
                    time_stamp = time_stamp.replace("T", ",")
                    time_stamp = time_stamp.replace("Z", ",")
                else:
                    if time_stamp != "":
                        line = line.replace("--> ", "")
                        line = line.replace("/", ",")
                        line = time_stamp + line
                        line = line.replace(",,", ",")
                        if len(line.split()) == 2:
                            line = line.replace(" ", ",")
                        open_outfile.write(line)
            print datetime.now(), 'Done processing', myfile
            open_outfile.close()
            profiler_file.close()

def find_counters(myfiles):
    counter_list = list()
    print datetime.now(), 'Finding stats'
    for myfile in myfiles:
        if ("-profiler-" in myfile and not (".csv" in myfile)):
            profiler_file = open(myfile, 'r')
            lines = profiler_file.readlines()
            for line in lines:
                if "sub=App]" not in line:
                    line = line.split("/")
                    if len(line) > 1:
                        line = line[1]
                        counter_list.append(line)
    counter_list_unique = list()
    for counter in counter_list:
        if counter not in counter_list_unique and '\n' not in counter:
            counter_list_unique.append(counter)

    print datetime.now(), 'Done finding stats'
    return counter_list_unique

def find_files():
    cwd = os.getcwd()
    print datetime.now(), 'Finding files under:', cwd
    my_files = os.listdir(cwd)
    return my_files


file_list = find_files()
counter_list = find_counters(file_list)
print 'Found: ', counter_list
profile_to_csv(file_list)
file_list = find_files()
prep_stat_file(file_list, counter_list)

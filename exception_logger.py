# This code logs exceptions in Python

# first import some stuff
import sys
import os
import datetime
import traceback

# set default values for global variables
default_logbin = "exception_logs/" # this is the directory where the error logs are saved
log_limit = -1 # this sets a limit to the maximum number of logs saved,
# this can prevent a hard drive from filling up with error logs

def logbin_name_filter(name):
    # this function checks if a specified logbin directory is valid
    # the return value will always have an ending slash character
    # first make sure that the input is sane
    if not isinstance(name,str):
        raise TypeError()
    if len(name) == 0:
        raise ValueError()
    # now add an ending slash if we have to
    if name[-1] == "/":
        n = name
    elif name[-1] == "\\":
        n = name
    else:
        n = name + "/"
    # now check to make sure that it isn't a file
    # if if doesn't exist, create it
    if os.path.exists(n):
        if os.path.isdir(n) == False:
            raise NotADirectoryError("Specified logbin is a file, not a directory.")
    else:
        os.makedirs(n)
    return n

def logfile_name(dt):
    # use the datetime to create a filename
    # using this function ensures that not spaces and no
    # weird characters ever end up in the filename
    j = str(dt.year)
    j += ":" + str(dt.month)
    j += ":" + str(dt.day)
    j += "_" + str(dt.hour)
    j += ":" + str(dt.minute)
    j += ":" + str(dt.second)
    j += "_" +str(dt.microsecond)
    j += ".txt"
    return j

def log_exception(*p):
    # logs the most recent exception
    # first optional parameter is a string specifying a non-default logbin directory
    # second optional parameter is an interger specifying the log limit for that directory
    global default_logbin
    global log_limit
    # first figure out where we are going to save our information
    if len(p) == 0:
        lb = default_logbin
    else:
        lb = p[0]
    lb = logbin_name_filter(lb)
    # next, figure out if we have space to save our information
    if len(p) < 2:
        if log_limit >= 1:
            if len(os.listdir(lb)) >= log_limit:
                return
    else:
        if not isinstance(p[1],int):
            raise TypeError()
        if p[1] >= 1:
            if len(os.listdir(lb)) >= p[1]:
                return
    # get the exception information from the system
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    # get the time
    currentDT = datetime.datetime.now()
    # build the contents of the error log file
    j = str(currentDT) + os.linesep
    for x in traceback.extract_tb(exc_tb).format():
        j += x + os.linesep
    j += os.linesep
    # save it into a file specified by the logbin and time
    with open(lb + logfile_name(currentDT),"w+") as file:
        file.write(j)

def set_default_logbin(name):
    # set the default logbin
    # raises an exception if suggested new value
    # 1. isn't a string
    # 2. is an empty string
    # 3. specifies an existing file
    global default_logbin
    default_logbin = logbin_name_filter(name)

def set_log_limit(n):
    # sets the log limit
    # raises an exception if input is not an integer
    global log_limit
    if isinstance(n,int) == False:
        raise TypeError()
    if n >= 1:
        log_limit = n
    else:
        log_limit = -1

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:27:05 2017

@author: Daniel
"""
import os
from configparser import ConfigParser
import re

configtemplate = '''# hodea review minder cfg file

[minder_cfg]

# !!! USE INDENTIONS FOR MULTILINE OPTIONS !!!
# !!! Option Separator: EOL or ";" !!!
;-----------------------------------------------------------------
# Project Name

name = insert project name here

;-----------------------------------------------------------------
# File types, which has to be parsed

filetype = .c;.h;.cpp

;-----------------------------------------------------------------
# exclude path - relativ to given top dir
# all sub-directories will be excluded as well
# each exclude path has to start with '.\' or './'

exclude =    ./review_minder


;-----------------------------------------------------------------

'''
  
delimiters = "\n", ";", ","
regexPattern = '|'.join(map(re.escape, delimiters))
 
########################################################
# Function: 
# create config if not availeable and call read database
########################################################
class minder_cfg:
    
    def __init__(self, topdir):
        self.configdir = topdir + r'/review_minder/minder.cfg'
    
        if not (os.path.isdir(topdir + r'/review_minder')):
            os.mkdir(topdir + r'/review_minder')
        if not (os.path.exists(self.configdir)):
            flog = open(self.configdir, 'w')   
            flog.write(configtemplate) 
            flog.close()  
            
       
    def read_config(self, configname = None):
        
        config = ConfigParser()
        flog = open(self.configdir, 'rb')
        try:
            config.read(self.configdir)
        except:
            print("ERROR: Please use Intentions for multiline options in your minder.cfg file.")
            raise Exception
        flog.close()
        try:    
            config['minder_cfg'][configname]
        except:
            print("ERROR: Can't find configuration keyword '" + configname +"'")
            raise Exception
       
        return  re.split(regexPattern,config['minder_cfg'][configname].replace('\\',os.path.sep).replace('/',os.path.sep))


    
    

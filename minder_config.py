# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:27:05 2017

@author: Daniel
"""
import os
from configparser import ConfigParser

configtemplate = '''# hodea review minder cfg file

[minder_cfg]

# !!! USE INDENTIONS FOR MULTILINE OPTIONS !!!
# !!! Option Seperator: EOL or ";" !!!
;-----------------------------------------------------------------
# Project Name

name = insert project name here

;-----------------------------------------------------------------
# File types, which has to be parsed

filetype = .c;.h;.cpp

;-----------------------------------------------------------------
# exclude path
# all sub-directories will be excluded as well

exclude =  ./review_minder


;-----------------------------------------------------------------

'''
  
    
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
        config.read(self.configdir)
        try:    
            config['minder_cfg'][configname]
        except:
            print("ERROR: Can't find configuration keyword '" + configname +"'")
            flog.close()
            return None

        flog.close()
        return config['minder_cfg'][configname]


    
    
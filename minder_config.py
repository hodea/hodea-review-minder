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
# read & handle config file
########################################################
def read_config(cfgfile):
    
    config = ConfigParser()
   
    flog = open(cfgfile, 'rb')
    config.read(cfgfile)
    flog.close()
    return config
    
    
########################################################
# Function: 
# create config if not availeable and call read database
########################################################
def Getconfig(topdir):
    
    configdir = topdir + r'/review_minder/minder.cfg'

    if not (os.path.isdir(topdir + r'/review_minder')):
        os.mkdir(topdir + r'/review_minder')
    if not (os.path.exists(configdir)):
        flog = open(configdir, 'w')   
        flog.write(configtemplate) 
        flog.close()  
        
    try:    
        read_config(configdir)['minder_cfg']['name']
    except:
        print("ERROR: Can't find configuration keyword 'name'")
        return None
       
    try:    
        read_config(configdir)['minder_cfg']['filetype']
    except:
        print("ERROR: Can't find configuration keyword 'filetype'")
        return None
        
    try:    
        read_config(configdir)['minder_cfg']['exclude']
    except:
        print("ERROR: Can't find configuration keyword 'exclude'")
        return None
        
         
    return read_config(configdir)
    
    
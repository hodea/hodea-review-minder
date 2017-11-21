# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 19:04:16 2017

@author: Daniel
"""
import os
import json


jsonbody ='''{
"minder_overview": [
{
"items_open": 0,
"items_closed": 0,
"items_rejected" :0
},
{
"items_comment": 0,
"items_major": 0,
"items_minor": 0,
"items_undefined": 0
}
],
"minder_items": [
]
}'''


########################################################
# Function: 
# read database
######################################################## 
def read_db(dbdir):
    

    jvar = ""
    
    flog = open(dbdir, 'r')
    for line in flog:
        jvar = jvar + line 

    flog.close
   
    try:
        Minderdict = json.loads(jvar)
    except:
        print("ERROR: Cannot read the database file. Empty?")
        return None
    try:
        Minderdict['minder_overview'][0]['items_open']
        Minderdict['minder_overview'][0]['items_closed']
        Minderdict['minder_overview'][0]['items_rejected']
        Minderdict['minder_overview'][1]['items_comment']
        Minderdict['minder_overview'][1]['items_major']
        Minderdict['minder_overview'][1]['items_minor']
        Minderdict['minder_overview'][1]['items_undefined']
        Minderdict['minder_items']
    except:
        print("ERROR: One or more database keywords has been changed.")
        return None
    return Minderdict
    
########################################################
# Function: 
# create database if not availeable 
# and call read database
########################################################                
def Getdb(topdir):


    dbdir = topdir + r'/review_minder/minder.db'

    if not (os.path.isdir(topdir + r'\review')):
        os.mkdir(topdir + r'\review')
    if not (os.path.exists(dbdir)):
        flog = open(dbdir, 'w')   
        flog.write(jsonbody) 
        flog.close()  
         
    return read_db(dbdir)
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 19:04:16 2017

@author: Daniel
"""
import os
import json


jsonbody ='''{
"minder_items": [ 
]
}'''


   
########################################################
# Function: 
# create database if not availeable 
# and call read database
########################################################                
class minder_db:
    
    def __init__(self, topdir):
        self.dbdir = topdir + r'/review_minder/minder.db'
    
        if not (os.path.isdir(topdir + r'\review_minder')):
            os.mkdir(topdir + r'\review_minder')
        if not (os.path.exists(self.dbdir)):
            flog = open(self.dbdir, 'w')   
            flog.write(jsonbody) 
            flog.close() 
        
    def Getdb(self):

        jvar = ""
        
        flog = open(self.dbdir, 'r')
        for line in flog:
            jvar = jvar + line     
        flog.close
       
        try:
            Minderdict = json.loads(jvar)
        except:
            print("ERROR: Cannot read the database file. Empty?")
            return None
        try:
            Minderdict['minder_items']
        except:
            print("ERROR: One or more database keywords has been changed.")
        return Minderdict
    def Setdb(self, newdict):

        flog = open(self.dbdir, 'w')    
        flog.write(json.dumps(newdict,sort_keys=True,indent=0,separators=(',',': ')))
        flog.close  
        

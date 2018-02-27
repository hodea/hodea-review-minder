# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 19:38:29 2018

@author: Daniel
"""

import argparse
import os
from minder_config import minder_cfg  
from minder_database import minder_db
from minder_htmlreport import minder_report
import time
import hashlib
import uuid


class get_lastreview:
    
    def __init__(self, minder_dict, topdir, cfg_exclude, cfg_type):
        
        
        print(topdir)
        print(cfg_exclude)
        print(cfg_type)
        print(minder_dict)
        filecnt = 0
        for root, dirs, files in os.walk(topdir):
            for name in files:
                find = False
                for i in range(0,len(cfg_exclude)):

                    if os.path.join(root, name).startswith(os.path.dirname(cfg_exclude[i])):
                        find = True
                if find is True:
                    continue
                for j in range(0,len(cfg_type)): 
                    if name.lower().endswith(cfg_type[j]):
                        try:
                            flog = open(os.path.join(root, name), "rb")
                            flog.close()  
                            flog = open(os.path.join(root, name), 'r+')  
                            flog.close() 
                            filecnt+=1
                        except:
                            print("ERROR: No Access to: " + os.path.join(root, name))
                            raise Exception
        print(filecnt)
        
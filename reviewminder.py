# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:22:12 2017

@author: Daniel
"""

__status__ = "Beta-Test"
__version__ ="0.0.1 Alpha"

import argparse
import os
from minder_config import Getconfig 
from minder_database import Getdb

    
########################################################
# Function: 
# command line argument parser
########################################################
def parse_cmdline():
    """Evaluates the parameters given per command line.
   
    returns
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description = "hodea review minder version  " + __version__,  
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--path','-p',
        help = "directory to be parsed from review minder",
        )
    parser.add_argument(
        '--verbose','-v',
        help = "keep console Open after parsing",
        default = "true",
        choices = ["false","true"],
        )
    parser.add_argument(
        '--noparse','-n',
        help = "create reports out of database only",
        default = "false",
        choices = ["false","true"],
        )
    parser.add_argument(
        '--htmlreport','-r',
        help = "create html report after parsing",
        default = "true",
        choices = ["false","true"],
        )
    parser.add_argument(
        '--pdfreport','-f',
        help = "create pdf report after parsing",
        default = "false",
        choices = ["false","true"],
        )

    
    args = parser.parse_args()
    return args



########################################################
# Global calls on start execution
########################################################                    
# Start the walk
def minder():

    
    args = parse_cmdline()  
    # use other source than default
    if args.path is not None:
        topdir = args.path.replace('\\','/')
    else:
        topdir = '.'
    print('top-dir:  '+topdir)
    
    minder_cfg = Getconfig(topdir)
    if minder_cfg is None:
        print("ERROR: Stopping  minder! Please correct errors before proceeding.")
        return 
    print("read config:     OK")
    
    minder_dict = Getdb(topdir)
    if minder_dict is None:
        print("ERROR: Stopping  minder! Please correct errors before proceeding.")
        return 
    print("read database:   OK")
#Debug print; TODO remove
    print(minder_dict)

            
        
    
    
    #create html report out of database
    #if r'true' in args.htmlreport.lower(): 
    #    create_html_report()  
    
    #keep command line open
    #if r'true' in args.verbose.lower():
    #    raw_input("\n\npress enter to exit")   
    
minder()
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:22:12 2017

@author: Daniel
"""

__status__ = "Beta-Test"
__version__ ="0.0.1 Alpha"

import argparse
import os
from minder_config import minder_cfg 
from minder_database import minder_db
import time
import hashlib
import uuid


    
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




class rm_handle_entry:
    
    def __init__(self,entry):
        self.entry = entry
        
    def get_entry_status(self, flog, rm_db, filename):
        find = False

        if not any("rm_id_" in s.lower() for s in self.entry):
#Debug print; TODO remove
            print('found new item no id')
            return  self.new_entry(flog, rm_db, filename)
        else:
            matching = [s for s in self.entry if "rm_id_" in s.lower()] 
            self.rm_id = matching[0].lower().rstrip('\r\n').split('___')[1].rstrip("'") 
            p = len(rm_db['minder_items'])
            if(p):                                     #if log empty, the next found id must be new
                for i in range(0,p):
                    if (self.rm_id in rm_db['minder_items'][i]['ID']): 
#Debug print; TODO remove
                        print("found existing item ")
                        return self.existing_entry(i, flog, rm_db, filename)
                        find = True
                    #update comment here
                if not find:
                        print(self.rm_id)
                        print("found new item not existing id")
                        return self.new_entry(flog, rm_db, filename)
            else:
#Debug print; TODO remove
                print("found new item no ids exist so far")
                return self.new_entry(flog, rm_db, filename)

    def new_entry(self, flog, rm_db, filename):
        comment = ''
        salt = uuid.uuid4().hex
        hash_object = hashlib.sha1(salt.encode('utf-8'))
        new_ID = ('RM_ID_%d___'+hash_object.hexdigest()) %len(rm_db['minder_items'])
        rm_db['minder_items'].append({'ID':new_ID,\
                                     'status':'Open',\
                                     'opendate':time.strftime("%d/%m/%Y"),\
                                     'closedate':' ',\
                                     'file':filename})
        while True:
            nextline = next(flog)
            if "*/" not in nextline:
                comment = comment + nextline.lstrip('*')
            else:
                break
        p = len(rm_db['minder_items']) - 1
        rm_db['minder_items'][p]['comment'] = comment
        return p

            
    def existing_entry(self,p, flog, rm_db, filename):
        comment = ''
        while True:
            nextline = next(flog)
            if "*/" not in nextline:
                comment = comment + nextline.lstrip('*')
            else:
                break
        rm_db['minder_items'][p]['comment'] = comment
        return p

            
            
            
        
        #print(rm_db['minder_items'])

        #print(rm_db['minder_items'])
        #m_db['minder_items'] + {'ID':self.rm_id}
        #print(rm_db)
        
        
        
class rm_check_line:
    
    def __init__(self, line):
        self.line = str(line.rstrip(os.linesep))
        
# find used end of line format
        
    def get_entry(self):
        if r'/*todo:review' in self.line.lower().replace(' ',''):
            return self.line.lower().replace(' ','').split(':')
        else:
            return False

            

########################################################
# Global calls on start execution
########################################################                    
# Start the walk
class hodea_review_minder:

    
    def __init__(self, topdir):
        
        self.topdir = topdir
        
        try:
            config = minder_cfg(self.topdir)
            self.cfg_name = config.read_config(configname='name')
            self.cfg_type = config.read_config(configname='filetype')
            self.cfg_exclude = config.read_config(configname='exclude')
        except:
            raise Exception 
    #Debug print; TODO remove
        print("*****DEBUG:cfg name")
        print(self.cfg_name)
        print("*****")
        print("*****DEBUG:cfg type")
        print(self.cfg_type)
        print("*****")
        print("*****DEBUG:cfg exclude")
        print(self.cfg_exclude) 
        print("*****")
    #Debug End
        
        print("read config:     OK")
        
        
        try:
            self.minder_dict = minder_db(self.topdir)
            self.dict = self.minder_dict.Getdb()
        except:
            raise Exception
        print("read database:   OK")
    #Debug print; TODO remove
        print("*****DEBUG:")
        print(self.dict)
        print("*****")
    #Debug End
        
    def rm_access_check(self):
        
        for root, dirs, files in os.walk(self.topdir):
            for name in files:
                find = False
                for i in range(0,len(self.cfg_exclude)):
                    if self.cfg_exclude[i] in os.path.join(root, name):
                        find = True
                if find is True:
                    continue
                for j in range(0,len(self.cfg_type)): 
                    if name.lower().endswith(self.cfg_type[j]):
                        try:
                            flog = open(os.path.join(root, name), "rb")
                            flog.close()  
                            flog = open(os.path.join(root, name), 'r+')  
                            flog.close() 
                        except:
                            print("ERROR: No Access to: " + os.path.join(root, name))
                            raise Exception
                            
    def rm_search(self):
        for root, dirs, files in os.walk(self.topdir):
            for name in files:
                find = False
                for i in range(0,len(self.cfg_exclude)):
                    if self.cfg_exclude[i] in os.path.join(root, name):
                        find = True
                if find is True:
                    continue
                for j in range(0,len(self.cfg_type)): 
                    if name.lower().endswith(self.cfg_type[j]):
                        print(os.path.join(root, name))
                        flog = open(os.path.join(root, name), "r")
                        newfile = ''
                        for line in flog:           #add write new file here + add hash before writing new file
                            #try:
                            currentline = rm_check_line(line)
                            entry = currentline.get_entry()
                            if entry is not False:
                                entry_handler = rm_handle_entry(entry)
                                p = entry_handler.get_entry_status(flog, self.dict, name)
                                newfile = newfile + '/*TODO:review:STATUS:' + \
                                    self.dict['minder_items'][p]['status'] + ':' +\
                                    self.dict['minder_items'][p]['ID'] + '\n' + \
                                    self.dict['minder_items'][p]['comment'] + '*/\n' 

                            else:
                                newfile = newfile + line
                        flog.close()
                        flog = open(os.path.join(root, name), "w")
                        flog.write(newfile)
                        flog.close()

    def rm_setdb(self):
         self.minder_dict.Setdb(self.dict)
                            
                                
                                
                             
                            


def main():
    
    args = parse_cmdline()  
    # use other source than default
    if args.path is not None:
        topdir = args.path.replace('\\','/')
    else:
        topdir = '.'
    print('top-dir:  '+topdir)
        
    try:
        minder = hodea_review_minder(topdir)
    except:
        print("Init ERROR: Stopping  minder! Please correct errors before proceeding.")
        return
    
    try:
        minder.rm_access_check()
    except:
        print("Access ERROR: Stopping  minder! Please correct errors before proceeding.")
        return
    
    #try:
    minder.rm_search()
    minder.rm_setdb()
 
   # except:
     #   print("Parsing ERROR: Stopping  minder! Please correct errors before proceeding.")
    #    return

    
main()

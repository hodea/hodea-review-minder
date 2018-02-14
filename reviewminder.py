# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:22:12 2017

@author: Daniel
"""

__status__ = "Development"
__version__ ="0.0.1 Alpha"

import argparse
import os
from minder_config import minder_cfg  
from minder_database import minder_db
from minder_htmlreport import minder_report
import time
import hashlib
import uuid
import re




sup_status = ['open','closed','rejected']
sup_severity = ['major','minor','comments']
    
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
        help = "create html report",
        default = "false",
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

def isA_subdirOfB_orAisB(A, B):
    """It is assumed that A is a directory."""
    relative = os.path.relpath(os.path.realpath(A), 
                               os.path.realpath(B))
    return not (relative == os.pardir
            or  relative.startswith(os.pardir + os.sep))


    
class rm_handle_entry:
     
    
    def __init__(self,entry):
        self.entry = entry

        
    def get_entry_status(self, flog, rm_db, filename):
        idfound = False
        severityfound = False
        statusfound = False
        for i in range(0,len(sup_severity)):
            if [s for s in self.entry if sup_severity[i] in s.lower()] :
                self.severity = sup_severity[i]
                severityfound = True
        if not severityfound:
            self.severity = 'undefined'
        if not any("rm_id_" in s.lower() for s in self.entry):
            return  self.new_entry(flog, rm_db, filename)
        else:
            matching = [s for s in self.entry if "rm_id_" in s.lower()] 
            self.rm_id = matching[0].lower().rstrip('\r\n').split('___')[1].rstrip("'") 
            for i in range(0,len(sup_status)):
                if [s for s in self.entry if sup_status[i] in s.lower()] :
                    self.status = sup_status[i]
                    statusfound = True
            if not statusfound:
                self.status = sup_status[0]
            p = len(rm_db['minder_items'])
            if(p):                                     #if log empty, the next found id must be new
                for i in range(0,p):
                    if (self.rm_id in rm_db['minder_items'][i]['ID']): 
                        return self.existing_entry(i, flog, rm_db, filename)
                        idfound = True
                if not idfound:
                        return self.new_entry(flog, rm_db, filename)
            else:
                return self.new_entry(flog, rm_db, filename)

    def new_entry(self, flog, rm_db, filename):
        comment = ''
        author = ''
        salt = uuid.uuid4().hex
        hash_object = hashlib.sha1(salt.encode('utf-8'))
        new_ID = ('RM_ID_%d___'+hash_object.hexdigest()) %len(rm_db['minder_items'])
        rm_db['minder_items'].append({'ID':new_ID,\
                                     'status':sup_status[0],\
                                     'severity':self.severity,\
                                     'opendate':time.strftime("%d/%m/%Y"),\
                                     'closedate':' ',\
                                     'file':flog.name.replace('\\','/')})
        
        while True:
            nextline = next(flog)
            if "*/" not in nextline:
                if "author:" not in nextline.lower():
                    comment = comment + nextline.lstrip(' ')
                else:
                    author = nextline.split(':')[1].strip()                     
            else:
                break            
        p = len(rm_db['minder_items']) - 1
        
        rm_db['minder_items'][p]['comment'] = comment
        rm_db['minder_items'][p]['author'] = author
        return p

            
    def existing_entry(self,p, flog, rm_db, filename):
        comment = ''
        author = ''
        while True:            
            nextline = next(flog)
            if "*/" not in nextline:
                if "author:" not in nextline.lower():
                    comment = comment + nextline.lstrip(' ')
                else:
                    author = nextline.split(':')[1].strip()                                        
            else:
                break

        rm_db['minder_items'][p]['comment'] = comment
        rm_db['minder_items'][p]['author'] = author
        rm_db['minder_items'][p]['status'] = self.status
        rm_db['minder_items'][p]['severity'] = self.severity
        
        rm_db['minder_items'][p]['file'] = flog.name.replace('\\','/')
        

        print(rm_db['minder_items'][p]['file'])

        print(rm_db['minder_items'][p])
        return p


        
        
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
            self.cfg_name = [s.strip() for s in self.cfg_name]

            self.cfg_type = config.read_config(configname='filetype')
            self.cfg_type = [s.strip() for s in self.cfg_type]

            self.cfg_exclude = config.read_config(configname='exclude')
            self.cfg_exclude = [s.strip() for s in self.cfg_exclude]
            
            for i in range(0,len(self.cfg_exclude)):
                if self.cfg_exclude[i].startswith('.'):     #cfg exclude has to start with '.'
                    if not self.cfg_exclude[i].endswith(os.path.sep):
                        self.cfg_exclude[i] = self.cfg_exclude[i] + os.path.sep#add path seperator at end if not there
                    if os.path.sep not in os.path.dirname(self.cfg_exclude[i]):
                        print("All files are excluded from parse. Please check the cfg")
                        raise Exception

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
            #get all IDs from list
            self.IDlist = []
            if self.dict['minder_items']:
                
                for i in range(0,len(self.dict['minder_items'])):
                    self.IDlist.append(self.dict['minder_items'][i]['ID'])

        except:
            raise Exception
        print("read database:   OK")
    #Debug print; TODO remove
        print("*****DEBUG:")
        print(self.dict)
        print("*****")
    #Debug End
    def rm_report(self):
        minder_report(self.topdir, self.dict)   
    def rm_access_check(self):
        
        for root, dirs, files in os.walk(self.topdir):
            for name in files:
                find = False
                for i in range(0,len(self.cfg_exclude)):

                    if os.path.join(root, name).startswith(os.path.dirname(self.cfg_exclude[i])):
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

                    if os.path.join(root, name).startswith(os.path.dirname(self.cfg_exclude[i])):
                        #print("EXCLUDE:         " + os.path.join(root, name))

                        find = True
                if find is True:
                    continue
                for j in range(0,len(self.cfg_type)): 
                    if name.lower().endswith(self.cfg_type[j]):
                        #print(os.path.join(root, name))
                        flog = open(os.path.join(root, name), "r")
                        #print(os.path.dirname(flog.name))
                        
                        newfile = ''
                        for line in flog:           #add write new file here + add hash before writing new file
                            #try:
                            currentline = rm_check_line(line)
                            entry = currentline.get_entry()
                            if entry is not False:
                                entry_handler = rm_handle_entry(entry)
                                p = entry_handler.get_entry_status(flog, self.dict, name)
                                #remove found IDs from found list - all left on list are deleted in file and needs to be closed
                                
                                if self.dict['minder_items'][p]['ID'] in self.IDlist:
                                    self.IDlist.remove(self.dict['minder_items'][p]['ID'])
                                #if status open
                                if self.dict['minder_items'][p]['status'] is sup_status[0]:
                                    newfile = newfile + '/*TODO:review:STATUS:' + \
                                        self.dict['minder_items'][p]['status'] + ':' +\
                                        self.dict['minder_items'][p]['severity'] + ':' +\
                                        self.dict['minder_items'][p]['ID'] + '\n' + \
                                        'Author:' +\
                                        self.dict['minder_items'][p]['author'] + '\n' + \
                                        self.dict['minder_items'][p]['comment'] + '*/\n' 
                                else:
                                    self.dict['minder_items'][p]['closedate'] = time.strftime("%d/%m/%Y")

                            else:
                                newfile = newfile + line
                        flog.close()
                        flog = open(os.path.join(root, name), "w")
                        flog.write(newfile)
                        flog.close()
        #close all IDs which are no more in code
        if self.dict['minder_items']:
            for i in range(0,len(self.dict['minder_items'])):
                if self.dict['minder_items'][i]['status'].rstrip('') == r'open':                
                    if self.dict['minder_items'][i]['ID'] in self.IDlist:
                        self.dict['minder_items'][i]['status'] = sup_status[1]

                
                    

    def rm_setdb(self):
         self.minder_dict.Setdb(self.dict)
                            
                                
                                
                             
                            


def main():
    
    args = parse_cmdline()  
    # use other source than default
    if args.path is not None:
        topdir = args.path.replace('\\',os.path.sep).replace('/',os.path.sep)
    else:
        topdir = '.'
    print('top-dir:  '+ topdir)
    try:
        minder = hodea_review_minder(topdir)
    except:
        print("Init ERROR: Stopping  minder! Please correct errors before proceeding.")
        return
    if 'true' in str(args.htmlreport):
        minder.rm_report()
    else:
       
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

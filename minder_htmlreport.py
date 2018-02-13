# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 19:43:58 2018

@author: Daniel
"""

import os
import json

htmbody_head='''
<meta charset="UTF-8">
<meta version="0.11">
<head>
<style>
a.nav:link {color: black; text-decoration: none; }
a.nav:visited {color: black; text-decoration: none; }
a.nav:hover {color: red; text-decoration: none; }
a.nav:active {color: black; } 

body{font-family:"Trebuchet MS", Helvetica, sans-serif}
table.reviewtable th { border:1px solid #000000; padding:5px;}
table.reviewtable tr, td { padding:5px;}        

table.reviewtable tr:hover {color: white; background-color: #1E90FF}

.myButton {
	-moz-box-shadow:inset 0px 1px 0px 0px #97c4fe;
	-webkit-box-shadow:inset 0px 1px 0px 0px #97c4fe;
	box-shadow:inset 0px 1px 0px 0px #97c4fe;
	background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #3d94f6), color-stop(1, #1e62d0));
	background:-moz-linear-gradient(top, #3d94f6 5%, #1e62d0 100%);
	background:-webkit-linear-gradient(top, #3d94f6 5%, #1e62d0 100%);
	background:-o-linear-gradient(top, #3d94f6 5%, #1e62d0 100%);
	background:-ms-linear-gradient(top, #3d94f6 5%, #1e62d0 100%);
	background:linear-gradient(to bottom, #3d94f6 5%, #1e62d0 100%);
	filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#3d94f6', endColorstr='#1e62d0',GradientType=0);
	background-color:#3d94f6;
	-moz-border-radius:6px;
	-webkit-border-radius:6px;
	border-radius:6px;
	border:1px solid #337fed;
	display:inline-block;
	cursor:pointer;
	color:#ffffff;
	font-family:Arial;
	font-size:15px;
	font-weight:bold;
	padding:6px 24px;
	text-decoration:none;
	text-shadow:0px 1px 0px #1570cd;
}
.myButton:hover {
	background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #1e62d0), color-stop(1, #3d94f6));
	background:-moz-linear-gradient(top, #1e62d0 5%, #3d94f6 100%);
	background:-webkit-linear-gradient(top, #1e62d0 5%, #3d94f6 100%);
	background:-o-linear-gradient(top, #1e62d0 5%, #3d94f6 100%);
	background:-ms-linear-gradient(top, #1e62d0 5%, #3d94f6 100%);
	background:linear-gradient(to bottom, #1e62d0 5%, #3d94f6 100%);
	filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#1e62d0', endColorstr='#3d94f6',GradientType=0);
	background-color:#1e62d0;
}
.myButton:active {
	position:relative;
	top:1px;
}
</style> 
</head>
<html>
<script type="text/javascript">
'''

htmbody='''
//@JSON-END-internal variables
var sortID = 0;
var sortstatus = 1;
var sortdate = 0;
var sortclosedate = 0;
var sortseverity = 0;
var sortfile = 0;
var sortcomments = 0;
var j = 0;

var buttonhandler = [false,true,false];

</script>
<body>

<table id="toptable" class="toptable" cellpadding="0" cellspacing="0" border="0"  style="padding-bottom:20px;font-size:10pt">

<td><a href="https://github.com/hodea/hodea-review-minder"><img src="https://raw.github.com/hodea/hodea-review-minder/master/logo/hodea_review_minder_logo.png" alt="Miner_logo" width="128" height="128"></td>
<td>
<td>Last Update:</td>
<td>test</td></td>

</table>
<button class="myButton" type="button" onclick="href:javascript:sort('expand')">Issues</button>
<button class="myButton" type="button">Coverage</button>
<button class="myButton" type="button" onclick="href:javascript:printoverview('expand')">Executive Summmary</button>
<script type="text/javascript">
document.write('<div id="overviewdiv">')
document.write('</div>')
document.write('<div id="tablediv">')
document.write('</div>')


function sort(order)
{
    
	if(order == 'minimize')
	{
		printheader();
		return;
	}
	printoverview('minimize');
    if(order == 'ID')
    {
        if(sortID)
        {
            myJSONObject.minder_items.sort(function(a, b) {
                return ((Number(b.ID.split('___')[0].split('_')[2]) < Number(a.ID.split('___')[0].split('_')[2])) ? -1 : ((Number(a.ID.split('___')[0].split('_')[2]) == Number(b.ID.split('___')[0].split('_')[2])) ? 0 : 1));
            });
            sortID = false;
        }
        else
        {
            myJSONObject.minder_items.sort(function(a, b) {
                return ((Number(a.ID.split('___')[0].split('_')[2]) < Number(b.ID.split('___')[0].split('_')[2])) ? -1 : ((Number(a.ID.split('___')[0].split('_')[2]) == Number(b.ID.split('___')[0].split('_')[2])) ? 0 : 1));
            });
            sortID = true;
        }
    }
    else if(order == 'file')
    {
        if(sortfile)
        {
            myJSONObject.minder_items.sort(function(a, b) {
                return ((b.file < a.file) ? -1 : ((a.file == b.file) ? 0 : 1));
            });
            sortfile = false;
        }
        else
        {
            myJSONObject.minder_items.sort(function(a, b) {
                return ((a.file < b.file) ? -1 : ((a.file == b.file) ? 0 : 1));
            });
            sortfile = true;
        }
    }
    else if(order == 'status')
    {
        if(sortstatus)
        {
            myJSONObject.minder_items.sort(function(a, b) {
                return ((Number(b.gloablsevstatus) < Number(a.gloablsevstatus)) ? -1 : ((Number(a.gloablsevstatus) == Number(b.gloablsevstatus)) ? 0 : 1));
            });
            sortstatus = false;
        }
        else
        {
            myJSONObject.minder_items.sort(function(a, b) {
                return ((Number(a.gloablsevstatus) < Number(b.gloablsevstatus)) ? -1 : ((Number(a.gloablsevstatus) == Number(b.gloablsevstatus)) ? 0 : 1));
            });
            sortstatus = true;
        }

    }
    else if(order == 'opendate')
    {
        if(sortdate)
        {
            myJSONObject.minder_items.sort(function(a, b) {
                return ((b.opendate < a.opendate) ? -1 : ((a.opendate == b.opendate) ? 0 : 1));
            });
            sortdate = false;
        }
        else
        {
            myJSONObject.minder_items.sort(function(a, b) {
                return ((a.opendate < b.opendate) ? -1 : ((a.opendate == b.opendate) ? 0 : 1));
            });
            sortdate = true;
        }
    }
    else if(order == 'closedate')
    {
        if(sortclosedate)
        {
            myJSONObject.minder_items.sort(function(a, b) {
                return ((b.closedate < a.closedate) ? -1 : ((a.closedate == b.closedate) ? 0 : 1));
            });
            sortclosedate = false;
        }
        else
        {
            myJSONObject.minder_items.sort(function(a, b) {
                return ((a.closedate < b.closedate) ? -1 : ((a.closedate == b.closedate) ? 0 : 1));
            });
            sortclosedate = true;
        }
    }
    else if(order == 'severity')
    {
        if(sortseverity)
        {
            myJSONObject.minder_items.sort(function(a, b) {
                return ((Number(b.gloablsevseverity) < Number(a.gloablsevseverity)) ? -1 : ((Number(a.gloablsevseverity) == Number(b.gloablsevseverity)) ? 0 : 1));
            });
            sortseverity = false;
        }
        else
        {
            myJSONObject.minder_items.sort(function(a, b) {
                return ((Number(a.gloablsevseverity) < Number(b.gloablsevseverity)) ? -1 : ((Number(a.gloablsevseverity) == Number(b.gloablsevseverity)) ? 0 : 1));
            });
            sortseverity = true;
        }
    }
    else if(order == 'comments')
    {
        if(sortcomments)
        {
            myJSONObject.minder_items.sort(function(a, b) {
                return ((b.comments < a.comments) ? -1 : ((a.comments == b.comments) ? 0 : 1));
            });
            sortcomments = false;
        }
        else
        {
            myJSONObject.minder_items.sort(function(a, b) {
                return ((a.comments < b.comments) ? -1 : ((a.comments == b.comments) ? 0 : 1));
            });
            sortcomments = true;
        }
    }
    printtable();
}
function printtable()
{
    newtable = '<table id="reviewtable" class="reviewtable" cellpadding="0" cellspacing="1" border="0" width="1100" style="padding-top:50px;font-size:10pt">'  
    newtable = newtable + '<tr>'
    newtable = newtable + '<th width="75"><a href="javascript:sort(\\'ID\\')" class="nav">ID</a></th>'
    newtable = newtable + '<th width="1%"><a href="javascript:sort(\\'file\\')" class="nav">File</a></th>'
    newtable = newtable + '<th width="60"><a href="javascript:sort(\\'status\\')" class="nav">Status</a></th>'
    newtable = newtable + '<th width="100"><a href="javascript:sort(\\'opendate\\')" class="nav">Open date</a></th>'
    newtable = newtable + '<th width="100"><a href="javascript:sort(\\'closedate\\')" class="nav">Close date</a></th>'
    newtable = newtable + '<th width="100"><a href="javascript:sort(\\'severity\\')" class="nav">Severity</a></th>'
    newtable = newtable + '<th><a href="javascript:sort(\\'comment\\')" class="nav">Comments</a></th><tr>' 
    for(i=0;i<myJSONObject.minder_items.length;i++)
    {
        if(i%2 == 0)
        {
            newtable = newtable + '<tr bgcolor="#EFEFEF"><td align="center">' + myJSONObject.minder_items[i].ID.split('___')[0].split('_')[2] + '</td>'
        } 
        else
        {
            newtable = newtable + '<tr bgcolor="#FCFCFC"><td align="center">' + myJSONObject.minder_items[i].ID.split('___')[0].split('_')[2] +  '</td>'
        }
            newtable = newtable + '<td align="center">' + myJSONObject.minder_items[i].file + '</td>' 
            newtable = newtable + '<td align="center">' + myJSONObject.minder_items[i].status + '</td>' 
            newtable = newtable + '<td align="center">' + myJSONObject.minder_items[i].opendate + '</td>'  
            newtable = newtable + '<td align="center">' + myJSONObject.minder_items[i].closedate + '</td>' 
            newtable = newtable + '<td align="center">' + myJSONObject.minder_items[i].severity + '</td>' 
            if(myJSONObject.minder_items[i].comment.split("</br>").length > 1)
            { 
                newtable = newtable + '<td><a id="commentlinker'+i+'" class="nav">' + myJSONObject.minder_items[i].comment.split("</br>")[0] + '</a></td></div></tr>'
            }
            else
            {
                newtable = newtable + '<td><a class="navnolink">' + myJSONObject.minder_items[i].comment.split("</br>")[0] + '</a></td></div></tr>'
            }
    }
    newtable = newtable + '</table>'
    document.getElementById('tablediv').innerHTML=newtable;


    
    for(i=0;i<myJSONObject.minder_items.length;i++)
    {
        if(myJSONObject.minder_items[i].comment.split("</br>").length > 1)
        {
            document.getElementById("commentlinker"+i).addEventListener("click", (function(j) {
                return function(e) {
                if(document.getElementById("commentlinker"+j).innerHTML == myJSONObject.minder_items[j].comment.split("</br>")[0])
                {
                        document.getElementById("commentlinker"+j).innerHTML = myJSONObject.minder_items[j].comment;
                }
                else
                {
                    document.getElementById("commentlinker"+j).innerHTML = myJSONObject.minder_items[j].comment.split("</br>")[0]
                }
                e.preventDefault();
                }
            })(i));
        }
    }
}
function printheader()
{   
    newtable = ''    
    document.getElementById('tablediv').innerHTML=newtable;
}
function printoverview(order)
{
    var totalnumber = ov_open+ov_closed+ov_rejected
	

	newoverview = ''
    if(order == 'expand')
    {
		sort('minimize');
        newoverview = '<table cellpadding="0" cellspacing="0" border="0" width="800" style="padding-top:50px;font-size:10pt"><tr><td>'
        newoverview = newoverview + '<table cellpadding="0" cellspacing="0" border="0" width="200" style="font-size:10pt">'
        newoverview = newoverview + '<tr><td width="150">Open</td>'
        newoverview = newoverview + '<td>' + ov_open + '</td>'
        newoverview = newoverview + '</tr><tr>'
        newoverview = newoverview + '<td>Rejected</td>'
        newoverview = newoverview + '<td>' + ov_rejected + '</td>'
        newoverview = newoverview + '</tr><tr>'
        newoverview = newoverview + '<td>Closed</td>'
        newoverview = newoverview + '<td>' + ov_closed + '</td>'
        newoverview = newoverview + '</tr></table></td><td>'
        newoverview = newoverview + '<table cellpadding="0" cellspacing="0" border="0" width="600" height ="20">'
        newoverview = newoverview + '<tr>' 
        if(ov_open > 0){
            newoverview = newoverview + '<td style="width:' + (100*ov_open)/(totalnumber) +'%" bgcolor="#F76C6C"></td>'
        }if(ov_rejected > 0){
            newoverview = newoverview + '<td style="width:' + (100*ov_rejected)/(totalnumber) + '%" bgcolor="#b2ff00"></td>'
        }if(ov_closed > 0){
            newoverview = newoverview + '<td style="width:' + (100*ov_closed)/(totalnumber) + '%" bgcolor="#7ACC57"></td>'
        }   
              
        newoverview = newoverview + '</tr></table></td></tr></table>'
        newoverview = newoverview + '<table cellpadding="0" cellspacing="0" border="0" width="800" height="20" style="padding-top:50px">'
        newoverview = newoverview + '<tr><td>'
        newoverview = newoverview + '<table cellpadding="0" cellspacing="0" border="0" width="200" style="font-size:10pt">'
        newoverview = newoverview + '<tr><td width="150">Major</td>'
        newoverview = newoverview + '<td>' + ov_major + '</td>'            
        newoverview = newoverview + '</tr><tr><td>Minor</td>'
        newoverview = newoverview + '<td>' + ov_minor + '</td>'            
        newoverview = newoverview + '</tr><tr><td>Comments</td>'
        newoverview = newoverview + '<td>' + ov_comment + '</td>'            
        newoverview = newoverview + '</tr><tr><td>Undefined</td>'
        newoverview = newoverview + '<td>' + ov_undefined + '</td>'            
        newoverview = newoverview + '</tr></table></td>'
        newoverview = newoverview + '<td><table cellpadding="0" cellspacing="0" border="0" width="600" height="20" >'
        newoverview = newoverview + '<tr>'
        if(ov_major > 0){    
            newoverview = newoverview + '<td style="width:' + (100*ov_major)/(totalnumber) +'%" bgcolor="#F76C6C"></td>'
        }if(ov_minor > 0){
            newoverview = newoverview + '<td style="width:' + (100*ov_minor)/(totalnumber) + '%" bgcolor="#FFEC5E"></td>'
        }if(ov_comment > 0){
            newoverview = newoverview + '<td style="width:' + (100*ov_comment)/(totalnumber) + '%" bgcolor="#7ACC57"></td>'
        }if(ov_undefined > 0){
            newoverview = newoverview + '<td style="width:' + (100*ov_undefined)/(totalnumber) + '%" bgcolor="#e5e5e5"></td>'
        }        
        newoverview = newoverview + '</tr></table></td></tr></table>' 
    }


    document.getElementById('overviewdiv').innerHTML=newoverview;
}

function calcglobalseverity()
{
    var a,b;
    for(i=0;i<myJSONObject.minder_items.length;i++)
    {
        if(myJSONObject.minder_items[i].severity == 'major') a = 4;
        else if(myJSONObject.minder_items[i].severity == 'minor') a = 3;
        else if(myJSONObject.minder_items[i].severity == 'comment') a = 2;
        else a = 1;
        
        if(myJSONObject.minder_items[i].status == 'open') b = 21;
        else if(myJSONObject.minder_items[i].status == 'rejected') b = 5;
        else b = 1;
        
        myJSONObject.minder_items[i].gloablsevstatus = a * b;
        
        
        if(myJSONObject.minder_items[i].severity == 'major') a = 40;
        else if(myJSONObject.minder_items[i].severity == 'minor') a = 13;
        else if(myJSONObject.minder_items[i].severity == 'comment') a = 4;
        else a = 1;
        
        if(myJSONObject.minder_items[i].status == 'open') b = 3;
        else if(myJSONObject.minder_items[i].status == 'rejected') b = 2;
        else b = 1;
        
        myJSONObject.minder_items[i].gloablsevseverity = a * b;
    }
    
}

function printfilelog(order)
{

}


calcglobalseverity();
sort('status');
sort('expand');


</script>

</body>
</html>
'''
########################################################
# Function: 
# create database if not availeable 
# and call read database
########################################################                
class minder_report:
    
    def __init__(self, topdir, Minderdict):
        ov_major = 0;
        ov_minor = 0;
        ov_comments = 0;
        ov_undefined = 0;
        ov_open = 0;
        ov_closed = 0;
        ov_rejected = 0;
    
        self.repdir = topdir + r'/review_minder/minder.html'
    
        if not (os.path.isdir(topdir + r'\review_minder')):
            os.mkdir(topdir + r'\review_minder')


        
        for i in range(0,len(Minderdict['minder_items'])):
            if "major" in Minderdict['minder_items'][i]['severity']:
                ov_major = ov_major + 1
            elif "minor" in Minderdict['minder_items'][i]['severity']:
                ov_minor = ov_minor + 1
            elif "comments" in Minderdict['minder_items'][i]['severity']:
                ov_comments = ov_comments + 1
            else:
                ov_undefined = ov_undefined + 1
                
            if "open" in Minderdict['minder_items'][i]['status']:
                ov_open = ov_open + 1
            elif "closed" in Minderdict['minder_items'][i]['status']:
                ov_closed = ov_closed + 1
            else:
                ov_rejected = ov_rejected + 1                
                
        flog = open(self.repdir, 'w')   
        flog.write(htmbody_head) 
        

        ov_string = 'var ov_closed = ' + str(ov_closed) + ';' + 'var ov_comment = ' + str(ov_comments) + ';' +\
        'var ov_major = ' + str(ov_major) + ';' + 'var ov_minor = ' + str(ov_minor) + ';' +\
        'var ov_open = ' + str(ov_open) + ';' + 'var ov_rejected = ' + str(ov_rejected)  + ';' +\
        'var ov_undefined = ' + str(ov_undefined) + ';'

        flog.write(ov_string)
        flog.write('var myJSONObject = ')
        flog.write(json.dumps(Minderdict,sort_keys=True,indent=0,separators=(',',': ')))
        flog.write(htmbody) 
        flog.close() 
    

        
        

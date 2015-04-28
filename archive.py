'''
Project Newsletter

Scripts created by Arkiver and chpwssn (Chip Wasson)

Todo:
Categories for receiver mail account. Example: add category "tweakers" if mail received on tweakers@mail.com
Automatic update
Stability and watchdogs
Send commands through mail
DONE Handle encoding better
DONE STABLE Figure out how to handle attachments
'''

from inbox import Inbox
from config import *
import time,json
import os
import datetime

# Create the inbox.py object
inbox = Inbox()
attachmentsjson = []

command = False
newindex = False
newmails = False

@inbox.collate
# Our message handling function
def handle(rawdata, to, sender, subject, mailhtml, mailplain, attachments, toname, sendername):
	global newindex
	global command
	global newmails
	if sender == "arkiver@hotmail.com" or sender == "chpwssn@gmail.com":
		if mailplain == "create new index.html":
			newindex = True
			command = True
		elif mailplain == "create new index.html and new mails":
			newindex = True
			newmails = True
			command = True
	if newindex == True:
		if not '<!--TABLE VERSION-->' in open(baseDirectory+"index.html").read():
			startnum = 0
			while True:
				if os.path.exists(baseDirectory+"index.html-old-"+str(startnum)):
					startnum = int(startnum) + 1
				else:
					os.rename(baseDirectory+"index.html", baseDirectory+"index.html-old-"+str(startnum))
					break
	if command == False:
		# Write new mails to index.html
		timereceived = str(int(time.time()))
		directoryName = timereceived
		humantime = datetime.datetime.fromtimestamp(int(timereceived)).strftime('%Y-%m-%d %H:%M:%S')
		if not os.path.exists(baseDirectory+"index.html"):
			with open(baseDirectory+"index.html", "w") as mainindex:
				mainindex.write('<!--TABLE VERSION-->')
				mainindex.write("<html><head><title>Newsletter Archive (WIP)</title></head><body>")
				mainindex.write('<style type="text/css">.table {border-collapse:collapse;border-spacing:0}.table td{padding:10px 5px;border-style:solid;border-width:0px;word-break:normal;background-color:#E6E6E6;border-top-width:1px;border-bottom-width:1px;}.table th{padding:10px 5px;border-style:solid;border-width:0px;word-break:normal;background-color:#BDBDBD;border-top-width:1px;border-bottom-width:1px;}.table .table-b{background-color:C1C1C1}')
				mainindex.write('</style><table class="table"><tr><th class="table-a">DATE</th><th class="table-a">FROM</th><th class="table-a">SUBJECT</th><th class="table-a">LENGTH</th>')
				mainindex.write('</tr></table>')
				mainindex.write("</body></html>")
		open(baseDirectory+"index.html-temp", "w").close()
		basedir = open(baseDirectory+"index.html")
		basedirtemp = open(baseDirectory+"index.html-temp", "a")
		for text in basedir:
			if '<th class="table-a">DATE</th><th class="table-a">FROM</th><th class="table-a">SUBJECT</th><th class="table-a">LENGTH</th></tr><tr><td class="table-b">' in text:
				text = text.replace('<th class="table-a">DATE</th><th class="table-a">FROM</th><th class="table-a">SUBJECT</th><th class="table-a">LENGTH</th>','<th class="table-a">DATE</th><th class="table-a">FROM</th><th class="table-a">SUBJECT</th><th class="table-a">LENGTH</th></tr><tr><td class="table-a">'+humantime+'</td><td class="table-a">'+sender+'</td><td class="table-a"><a href="'+directoryName+'">'+subject+'</a></td><td class="table-a">'+str(len(rawdata))+'</td>')
			else:
				text = text.replace('<th class="table-a">DATE</th><th class="table-a">FROM</th><th class="table-a">SUBJECT</th><th class="table-a">LENGTH</th>','<th class="table-a">DATE</th><th class="table-a">FROM</th><th class="table-a">SUBJECT</th><th class="table-a">LENGTH</th></tr><tr><td class="table-b">'+humantime+'</td><td class="table-b">'+sender+'</td><td class="table-b"><a href="'+directoryName+'">'+subject+'</a></td><td class="table-b">'+str(len(rawdata))+'</td>')
			basedirtemp.write(text)
		basedir.close()
		basedirtemp.close()
		os.remove(baseDirectory+"index.html")
		os.rename(baseDirectory+"index.html-temp", baseDirectory+"index.html")
		print "Added "+directoryName+" to index.html"
		#Check to see if the directory we are going to write to exists
		if not os.path.isdir(baseDirectory+directoryName):
			os.makedirs(baseDirectory+directoryName)
		with open(baseDirectory+directoryName+"/index.html","w") as messageindex:
			messageindex.write("<html><head><title>"+directoryName+"</title></head><body>ALL DATA:&nbsp;<a href='"+directoryName+".json"+"'>JSON</a><br/>")
			messageindex.write("ATTACHMENT(S):&nbsp;")
			for attachment in attachments:
				if not os.path.isdir(baseDirectory+directoryName+"/attachments"):
					os.makedirs(baseDirectory+directoryName+"/attachments")
				with open(baseDirectory+directoryName+"/attachments/"+attachment[2],"w") as file:
					file.write(attachment[1])
				messageindex.write("<a href='attachments/"+attachment[2]+"'>"+attachment[2]+"</a>&nbsp;")
				print "Wrote attachment "+attachment[2]
				attachmentsjson.append([attachment[0], attachment[2], attachment[3]])
			messageindex.write("<br/>")
			messageindex.write("TO:&nbsp;"+toname+"&nbsp;"+to+"<br/>")
			messageindex.write("FROM:&nbsp;"+sendername+"&nbsp;"+sender+"<br/>")
			messageindex.write("SUBJECT:&nbsp;"+subject+"<br/>")
			messageindex.write("DATE:&nbsp;"+humantime+"<br/>")
			# Write the components to the .json file, better for processing later but doesn't solve encoding
			with open(baseDirectory+directoryName+"/"+directoryName+".json","w") as jsonfile:
				jsonfile.write(json.dumps({"rawdata":rawdata, "to":to, "sender":sender, "subject":subject, "mailhtml":mailhtml, "mailplain":mailplain, "attachments":attachmentsjson, "toname":toname, "sendername":sendername}))
			# Write the html body to a html file by itself
			with open(baseDirectory+directoryName+"/"+directoryName+"-mailhtml.html","w") as mailhtmlfile:
				mailhtmlfile.write(mailhtml)
				messageindex.write("<iframe style='width:100%;height:45%'  src='"+directoryName+"-mailhtml.html'></iframe><br/>")
			with open(baseDirectory+directoryName+"/"+directoryName+"-mailplain.txt","w") as mailplainfile:
				mailplainfile.write(mailplain)
				messageindex.write("<iframe style='width:100%;height:45%'  src='"+directoryName+"-mailplain.txt'></iframe><br/>")
			print "Wrote "+directoryName+".json"
			messageindex.write("</body></html>")
# Start the inbox.py server on our local ip address
inbox.serve(address=localIPAddress, port=25)



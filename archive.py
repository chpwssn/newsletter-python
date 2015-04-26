# Project Newsletter Python Proof of Concept
# original inbox.py project by kennethreitz archive.py by chip v 0.0000001
#
# Basic idea:
# inbox.py instantiates a standalone mail server based in python and calls the handle function
# when it receives a new message. We then "handle" the message by saving it's text to a .txt file
# and a .json blob file.
#
# Todo:
# Handle encoding better
# Figure out how to handle attachments
# Stability and watchdogs

from inbox import Inbox
from config import *
import time,json
import os
import re

# Create the inbox.py object
inbox = Inbox()
timenow = time.time()
attachmentsjson = []

@inbox.collate
# Our message handling function
def handle(rawdata, to, sender, subject, mailhtml, mailplain, attachments):
	# Write new mails to index.html
	if not os.path.exists(baseDirectory+"index.html"):
		with open(baseDirectory+"index.html", "w") as mainindex:
			mainindex.write("<html><head><title>Newsletter Archive (WIP)</title></head><body>")
			mainindex.write('<style type="text/css">.table {border-collapse:collapse;border-spacing:0}.table td{padding:10px 5px;border-style:solid;border-width:0px;word-break:normal;background-color:#E6E6E6;border-top-width:1px;border-bottom-width:1px;}.table th{padding:10px 5px;border-style:solid;border-width:0px;word-break:normal;background-color:#BDBDBD;border-top-width:1px;border-bottom-width:1px;}.table .table-b{background-color:C1C1C1}')
			mainindex.write('</style><table class="table"><tr><th class="table-a">DATE</th><th class="table-a">FROM</th><th class="table-a">SUBJECT</th><th class="table-a">LENGTH</th>')
			mainindex.write('</tr></table>')
			mainindex.write("</body></html>")
		mainindex.close()
	open(baseDirectory+"index.html-temp", "w").close()
	for text in open(baseDirectory+"index.html"):
		if '<th class="table-a">DATE</th><th class="table-a">FROM</th><th class="table-a">SUBJECT</th><th class="table-a">LENGTH</th></tr><tr><td class="table-b">' in text:
			text = text.replace('<th class="table-a">DATE</th><th class="table-a">FROM</th><th class="table-a">SUBJECT</th><th class="table-a">LENGTH</th>','<th class="table-a">DATE</th><th class="table-a">FROM</th><th class="table-a">SUBJECT</th><th class="table-a">LENGTH</th></tr><tr><td class="table-a">'+str(int(timenow))+'</td><td class="table-a">'+sender+'</td><td class="table-a"><a href="'+sender+'-'+subject+'-'+str(int(timenow))+'">'+subject+'</a></td><td class="table-a">'+len(rawdata)+'</td>')
		else:
			text = text.replace('<th class="table-a">DATE</th><th class="table-a">FROM</th><th class="table-a">SUBJECT</th><th class="table-a">LENGTH</th>','<th class="table-a">DATE</th><th class="table-a">FROM</th><th class="table-a">SUBJECT</th><th class="table-a">LENGTH</th></tr><tr><td class="table-b">'+str(int(timenow))+'</td><td class="table-b">'+sender+'</td><td class="table-b"><a href="'+sender+'-'+subject+'-'+str(int(timenow))+'">'+subject+'</a></td><td class="table-b">'+len(rawdata)+'</td>')
		open(baseDirectory+"index.html-temp", "a").write(text).close()
	os.remove(baseDirectory+"index.html")
	os.rename(baseDirectory+"index.html-temp", baseDirectory+"index.html")
	print "Added "+sender+"-"+subject+"-"+str(int(timenow))+" to index.html"
	#Check to see if the directory we are going to write to exists
	directoryName = sender+"-"+subject+"-"+str(int(timenow))
	if not os.path.isdir(baseDirectory+directoryName):
		os.makedirs(baseDirectory+directoryName)
	with open(baseDirectory+directoryName+"/index.html","w") as messageindex:
		messageindex.write("<html><head><title>"+sender+"-"+subject+"-"+str(int(timenow))+"</title></head><body>ALL DATA:&nbsp;<a href='"+sender+"-"+subject+"-"+str(int(timenow))+".json"+"'>JSON</a><br/>")
		messageindex.write("ATTACHMENT(S):&nbsp;")
		for attachment in attachments:
			with open(baseDirectory+directoryName+"/attachments/"+attachment[2],"w") as file:
				file.write(attachment[1])
			file.close()
			messageindex.write("<a href='"+"attachments/"+attachment[2]+"'>"+attachment[2]+"</a>&nbsp;")
			print "Wrote attachment "+attachment[2]
			attachmentsjson.append([attachment[0], attachment[2], attachment[3]])
		messageindex.write("<br/>")
		messageindex.write("TO:&nbsp;"+to+"<br/>")
		messageindex.write("FROM:&nbsp;"+sender+"<br/>")
		messageindex.write("SUBJECT:&nbsp;"+subject+"<br/>")
		# Write the components to the .json file, better for processing later but doesn't solve encoding
		with open(baseDirectory+directoryName+"/"+sender+"-"+subject+"-"+str(int(timenow))+".json","w") as jsonfile:
			jsonfile.write(json.dumps({"rawdata":rawdata, "to":to, "sender":sender, "subject":subject, "mailhtml":mailhtml, "mailplain":mailplain, "attachments":attachmentsjson}))
		jsonfile.close()
		# Write the html body to a html file by itself
		with open(baseDirectory+directoryName+"/"+sender+"-"+subject+"-"+str(int(timenow))+"-mailhtml.html","w") as mailhtmlfile:
			mailhtmlfile.write(mailhtml)
			messageindex.write("<iframe style='width:100%;height:45%'  src='"+sender+"-"+subject+"-"+str(int(timenow))+"-mailhtml.html'></iframe><br/>")
		mailhtmlfile.close()
		with open(baseDirectory+directoryName+"/"+sender+"-"+subject+"-"+str(int(timenow))+"-mailplain.txt","w") as mailplainfile:
			mailplainfile.write(mailplain)
			messageindex.write("<iframe style='width:100%;height:45%'  src='"+sender+"-"+subject+"-"+str(int(timenow))+"-mailplain.txt'></iframe><br/>")
		mailplainfile.close()
		print "Wrote "+sender+"-"+subject+"-"+str(int(time.time()))+".json"
		messageindex.write("</body></html>")
	messageindex.close()
# Start the inbox.py server on our local ip address
inbox.serve(address=localIPAddress, port=25)



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

# Create the inbox.py object
inbox = Inbox()
timenow = time.time()
attachmentsjson = []

@inbox.collate
# Our message handling function
def handle(rawdata, to, sender, subject, mailhtml, mailplain, attachments):
	# Write new mails to index.html
	if not os.path.exists(baseDirectory+"index.html"):
			open(baseDirectory+"index.html", "w").close()
	with open(baseDirectory+"index.html", "a") as index:
		index.write("<a href='"+sender+"-"+subject+"-"+str(int(timenow))+"'>"+sender+"-"+subject+"-"+str(int(timenow))+"</a><br/>\n")
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
		# Write the html body to a html file by itself
		with open(baseDirectory+directoryName+"/"+sender+"-"+subject+"-"+str(int(timenow))+"-mailhtml.html","w") as mailhtmlfile:
			mailhtmlfile.write(mailhtml)
			messageindex.write("<iframe style='width:100%;height:45%'  src='"+sender+"-"+subject+"-"+str(int(timenow))+"-mailhtml.html'></iframe><br/>")
		with open(baseDirectory+directoryName+"/"+sender+"-"+subject+"-"+str(int(timenow))+"-mailplain.txt","w") as mailplainfile:
			mailplainfile.write(mailplain)
			messageindex.write("<iframe style='width:100%;height:45%'  src='"+sender+"-"+subject+"-"+str(int(timenow))+"-mailplain.txt'></iframe><br/>")
		print "Wrote "+sender+"-"+subject+"-"+str(int(time.time()))+".json"
		messageindex.write("</body></html>")
# Start the inbox.py server on our local ip address
inbox.serve(address=localIPAddress, port=25)



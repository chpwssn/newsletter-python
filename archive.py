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

@inbox.collate
# Our message handling function
def handle(rawdata, to, sender, subject, mailhtml, mailplain, attachments):
	# Write new mails to index.html
	if not os.path.exists("/home/ubuntu/newspoc/index.html"):
			open("/home/ubuntu/newspoc/index.html", "w").close() 
	with open("/home/ubuntu/newspoc/index.html", "a") as index:
		index.write("<a href='"+sender+"-"+subject+"-"+str(int(timenow))+"'>"+sender+"-"+subject+"-"+str(int(timenow))+"</a><br/>\n")
	print "Added "+sender+"-"+subject+"-"+str(int(timenow))+" to index.html"
	# Write the components to the .html file separated by newlines (ok but a little more readable)
	with open("/home/ubuntu/newspoc/"+sender+"-"+subject+"-"+str(int(timenow))+".html","w") as file:
		file.write("TO:\n"+str(to)+"\n")
		file.write("SENDER:\n"+str(sender)+"\n")
		file.write("SUBJECT:\n"+str(subject)+"\n")
		for attachment in attachments:
			if not attachment == None:
				file.write("<a href='/newspoc/"+sender+"-"+subject+"-"+str(int(timenow))+"/attachment-"+attachment[2]+"'>ATTACHMENT: "+attachment[2]+"</a><br/>\n")
		if not mailhtml == None:
			file.write("HTML:\n"+mailhtml+"\n")
		if not mailplain == None:
			file.write("PLAINTEXT:\n"+mailplain+"\n")
	print "Wrote "+sender+"-"+subject+"-"+str(int(time.time()))+".html"
	#Check to see if the directory we are going to write to exists
	directoryName = sender+"-"+subject+"-"+str(int(timenow))
	if not os.path.isdir("/home/ubuntu/newspoc/"+directoryName):
		os.makedirs("/home/ubuntu/newspoc/"+directoryName)
	for attachment in attachments:
		with open("/home/ubuntu/newspoc/"+directoryName+"/attachment-"+attachment[2],"w") as file:
			file.write(attachment[2])
		print "Wrote attachment"+attachment[2]
	# Write the components to the .json file, better for processing later but doesn't solve encoding
	with open("/home/ubuntu/newspoc/"+directoryName+"/"+sender+"-"+subject+"-"+str(int(timenow))+".json","w") as jsonfile:
		jsonfile.write(json.dumps({"rawdata":rawdata, "to":to, "sender":sender, "subject":subject, "mailhtml":mailhtml, "mailplain":mailplain, "attachments":attachments}))
	print "Wrote "+sender+"-"+subject+"-"+str(int(time.time()))+".json"
# Start the inbox.py server on our local ip address
inbox.serve(address=localIPAddress, port=25)

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

#Create the inbox.py object
inbox = Inbox()
@inbox.collate

#Our message handling function
def handle(to, sender, subject, body, attachments):
	#Write the components to the .txt file separated by newlines (ok but a little more readable)
	with open("/home/ubuntu/newspoc/"+sender+"-"+subject+"-"+str(int(time.time()))+".txt","w") as file:
		file.write(str(to)+"\n")
		file.write(str(sender)+"\n")
		file.write(str(subject)+"\n")
		if body:
			file.write(body+"\n")
		if attachments:
			file.write(attachments+"\n");
	print "Wrote "+sender+"-"+subject+"-"+str(int(time.time()))+".txt"
	#Write the components to the .json file, better for processing later but doesn't solve encoding
	with open("/home/ubuntu/newspoc/"+sender+"-"+subject+"-"+str(int(time.time()))+".json","w") as jsonfile:
		jsonfile.write(json.dumps({"to":to,"sender":sender,"subject":subject,"body":body,"attachments":attachments}))
	print "Wrote "+sender+"-"+subject+"-"+str(int(time.time()))+".json"


#Start the inbox.py server on our local ip address
inbox.serve(address=localIPAddress, port=25)

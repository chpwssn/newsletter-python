from inbox import Inbox
import time,json

inbox = Inbox()
@inbox.collate
def handle(to, sender, subject, body):
	with open("/home/ubuntu/newspoc/"+sender+"-"+subject+"-"+str(int(time.time()))+".txt","w") as file:
		file.write(str(to)+"\n")
		file.write(str(sender)+"\n")
		file.write(str(subject)+"\n")
		file.write(body+"\n")
	with open("/home/ubuntu/newspoc/"+sender+"-"+subject+"-"+str(int(time.time()))+".json","w") as jsonfile:
		jsonfile.write(json.dumps({"to":to,"sender":sender,"subject":subject,"body":body}))

inbox.serve(address='172.31.34.123', port=25)

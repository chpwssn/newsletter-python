import threading
import socket
import string
import sys
import re
import simplejson, urllib
from botconfig import *

#for debugging
import pprint

class IRCBot ( threading.Thread ):
    
    def run ( self ):
        self.s=socket.socket( )
        self.s.connect((HOST, PORT))
        self.s.send('NICK '+NICK+'\n')
        self.s.send('USER '+IDENT+' '+HOST+' bla :'+REALNAME+'\n')
        while 1:
            line=self.s.recv(500)
            print line
            if 'End of /MOTD command.' in line:
                self.s.send('JOIN '+CHANNELINIT+'\n')
            if 'PRIVMSG' in line:
                self.parsemsg(line)
                line=line.rstrip()
                line=line.split()
            if 'PING' in line:
                line = line.split(':')
                print "PONGING"+line[1]
                self.s.send('PONG '+line[1]+'\n')
                #self.sendmsg("Pong")
            if 'INVITE' in line:
                line = line.split(':')
                print line[2]
                self.s.send('JOIN '+line[2]+"\n")
                
                
    def sendmsg(self, message):
        self.s.send("PRIVMSG "+self.chansrc+" :"+message+"\n")

    def parsemsg(self, msg):
        complete=msg[1:].split(':',1) #Parse the message into useful data
        info=complete[0].split(' ')
        print complete
        msgpart=complete[1]
        sender=info[0].split('!')
        nick = sender[0]
        if msgpart[0]=='-' and sender[0]==OWNER :
            cmd=msgpart[1:]
            argcmd = cmd.split(':',1)
            argcmd = argcmd[1].rstrip().split(" ")
            print argcmd
            if argcmd[0] == "die":
                self.s.send("QUIT :Shutting Down\n")
                quit()
            elif argcmd[0] == "join":
                self.s.send('JOIN '+argcmd[1]+"\n")
            else:
                argcmd = " ".join(argcmd)
                self.s.send(argcmd+'\n')
                print 'cmd='+argcmd
        if msgpart[0] =='$':
            msgpart = re.sub(r'\r*\n*','',msgpart)
            cmd=msgpart[1:].split(' ')
            print msgpart
            self.chansrc = complete[0].split(" ")[2]
            #print chansrc
            if "status" in cmd[0]:
                print "Status command recieved"
                self.s.send("PRIVMSG "+CHANNELINIT+" :Still alive for now\n")
                self.sendmsg("Still alive for now")
            if "search" in cmd[0]:
                searchstring = str(" ".join(cmd[1:]))
                print "Searching for "+searchstring
                result = simplejson.load(urllib.urlopen("http://mailbot1.dev.projectnewsletter.org/?key={0}&action=search&variable={1}".format(apikey, searchstring)))
                print result['result']
                resultcount = 0
                resultmax = 10
                self.sendmsg("Search Results:")
                for item in result['result']:
                    resultcount+=1
                    print "Email: {0} Desc: {1} Registered By: {2}".format(item['1'],item['2'],item['3'])
                    self.sendmsg("Email: {0} Desc: {1} Registered By: {2}".format(item['1'],item['2'],item['3']))
                    if resultcount >= resultmax:
                        break
                if resultcount == 0:
                    self.sendmsg("No results found :(")
                if resultcount >= resultmax:
                    self.sendmsg("Too many results! (Reached {0}) Visit the web interface for more.".format(resultmax))
            if "register" in cmd[0]:
                email = cmd[1]
                description = " ".join(cmd[2:])
                result = simplejson.load(urllib.urlopen("http://mailbot1.dev.projectnewsletter.org/?key={0}&action=register&email={1}&desc={2}&user={3}".format(apikey,email,description,nick)))
                self.sendmsg("Registered {0}".format(email))
            if "help" in cmd[0]:
                self.sendmsg("I'm the Newsletter Email Registration Bot. See the following commands:")
                self.sendmsg("status - returns the status of this bot.")
                self.sendmsg("search <search phrase> - searches for the search phrase in the registration database in the 'email', 'description' and 'user' fields.")
                self.sendmsg("register <email@domain.tld> <a description phrase> - registers the email address with the description provided.")

if __name__ == "__main__":
    bot = IRCBot()
    bot.start()
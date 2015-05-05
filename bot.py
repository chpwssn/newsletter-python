import threading
import socket
import string
import sys
import re
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

    def sendmsg(self, message):
        self.s.send("PRIVMSG "+CHANNELINIT+" :"+message+"\n")

    def parsemsg(self, msg):
        complete=msg[1:].split(':',1) #Parse the message into useful data
        info=complete[0].split(' ')
        print complete
        msgpart=complete[1]
        sender=info[0].split('!')
        if msgpart[0]=='-' and sender[0]==OWNER :
            cmd=msgpart[1:]
            self.s.send(cmd+'n')
            print 'cmd='+cmd
        if msgpart[0] =='$':
            msgpart = re.sub(r'\n*\n*','',msgpart)
            cmd=msgpart[1:].split(' ')
            print msgpart
            if "status" in cmd[0]:
                print "Status command recieved"
                self.s.send("PRIVMSG "+CHANNELINIT+" :Still alive for now\n")
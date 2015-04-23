# -*- coding: utf-8 -*-

import smtpd
import asyncore
import argparse
from email.parser import Parser
from email.Header import decode_header
from email.message import Message

from logbook import Logger


log = Logger(__name__)


class InboxServer(smtpd.SMTPServer, object):
    """Logging-enabled SMTPServer instance with handler support."""

    def __init__(self, handler, *args, **kwargs):
        super(InboxServer, self).__init__(*args, **kwargs)
        self._handler = handler

    def process_message(self, peer, mailfrom, rcpttos, data):
        log.info('Collating message from {0}'.format(mailfrom))
        log.info('Length of message {0}'.format(len(data)))
        subject = self.parse_subject(Parser().parsestr(data)['subject'])
        mailplain = None
        mailhtml = None
        attachments = []
        for part_of_mail in Parser().parsestr(data).walk():
            mailcontent = self.parse_data(part_of_mail)
            for mailpart in mailcontent:
                if mailpart[0] == "application/octet-stream":
                    attachments.append(mailpart)
                elif mailpart[0] == "text/html":
                    mailhtml = mailpart[1]
                elif mailpart[0] == "text/plain":
                    mailplain = mailpart[1]
        
        log.debug(dict(rawdata=data, to = rcpttos, sender = mailfrom, subject = subject, mailhtml = mailhtml, mailplain = mailplain, attachments = attachments))
        return self._handler(rawdata=data, to = rcpttos, sender = mailfrom, subject = subject, mailhtml = mailhtml, mailplain = mailplain, attachments = attachments)
        
    def parse_subject(self, subject):
        # Decode subject if encoded
        encoded = decode_header(subject)
        subjectpart = []
        for a, b in encoded:
            if b:
                subjectpart.append(unicode(a, b).encode('utf8','replace'))
            else:
                subjectpart.append(a)
        subject = ''.join(subjectpart)
        return subject
        
    def parse_data(self, part_of_mail):
        # Check is part of mail is message or attachment
        # Decode support
        mailcontent = []
        
        if part_of_mail.get_content_type() == "text/html" or part_of_mail.get_content_type() == "text/plain":
            mailcontent.append([part_of_mail.get_content_type(), part_of_mail.get_payload(decode=True)])
        elif part_of_mail.get_content_type() == "application/octet-stream":
            mailcontent.append([part_of_mail.get_content_type(), part_of_mail.get_payload(decode=True), part_of_mail.get_filename(), part_of_mail.get_payload()])
        
        return(mailcontent)


class Inbox(object):
    """A simple SMTP Inbox."""

    def __init__(self, port=None, address=None):
        self.port = port
        self.address = address
        self.collator = None

    def collate(self, collator):
        """Function decorator. Used to specify inbox handler."""
        self.collator = collator
        return collator

    def serve(self, port=None, address=None):
        """Serves the SMTP server on the given port and address."""
        port = port or self.port
        address = address or self.address

        log.info('Starting SMTP server at {0}:{1}'.format(address, port))

        server = InboxServer(self.collator, (address, port), None)

        try:
            asyncore.loop()
        except KeyboardInterrupt:
            log.info('Cleaning up')

    def dispatch(self):
        """Command-line dispatch."""
        parser = argparse.ArgumentParser(description='Run an Inbox server.')

        parser.add_argument('addr', metavar='addr', type=str, help='addr to bind to')
        parser.add_argument('port', metavar='port', type=int, help='port to bind to')

        args = parser.parse_args()

        self.serve(port=args.port, address=args.addr)

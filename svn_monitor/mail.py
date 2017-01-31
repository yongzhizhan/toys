#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header


class Mail:
    mail_from = ""
    mail_to = ""
    mail_subject = ""
    mail_msg = ""

    server = None

    def __init__(self, smtp, mail_from, mail_to, mail_subject, mail_msg):
        self.server = smtplib.SMTP(smtp)

        self.mail_from = mail_from
        self.mail_to = mail_to
        self.mail_subject = mail_subject
        self.mail_msg = mail_msg

    def starttls(self):
        self.server.starttls()

    def login(self, username, password):
        return self.server.login(username, password)

    def send(self, sender, receiver):
        message = MIMEText(self.mail_subject, 'plain', 'utf-8')
        message['From'] = Header(self.mail_from, 'utf-8')
        message['To'] = Header(self.mail_to, 'utf-8')
        message['Subject'] = Header(self.mail_subject, 'utf-8')

        return self.server.sendmail(sender, receiver, message.as_string())



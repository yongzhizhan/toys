#!/usr/bin/env python
# coding:utf-8

import unittest

import config
from mail import Mail


class MailTest(unittest.TestCase):
    def test_send(self):
        try:
            mail = Mail("smtp.qq.com", "test from", "test to", "test subject", "test msg")
            mail.starttls()

            mail.login(config.email_user, config.email_pwd)
            mail.send(config.email_user, "263435079@qq.com")
        except Exception as e:
            print e
            exit(0)

        print "send mail complete"

if __name__ == "__main__":
    unittest.main()
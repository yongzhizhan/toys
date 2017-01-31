#!/usr/bin/env python
#conding: utf-8

import unittest
from threading import Timer
from time import sleep

import requests

from database import DataBase
from models import MailInfo, SvnInfo
from server import app


class ServerTestCase(unittest.TestCase):
    serverTimer = None

    def setUp(self):
        # add data
        database = DataBase("sqlite:///./data.db")
        database.init_db()

        session = database.get_session()

        session.query(SvnInfo).delete()
        session.query(MailInfo).delete()
        session.commit()

        # add data
        svn_path = "http://10.10.8.23/repos/tmp/test"
        mail_address = "263435079@qq.com"

        svn_info = SvnInfo(0, svn_path, 0)
        session.add(svn_info)
        session.add(MailInfo(None, 0, mail_address))
        session.commit()

        # run server
        self.serverTimer = Timer(0, self.run_server)
        sleep(3)
        self.serverTimer.start()

    def tearDown(self):
        requests.post('http://127.0.0.1:5000/shutdown')
        self.serverTimer.cancel()
        return

    def run_server(self):
        app.run(threaded = True)

    def test_list(self):
        list = requests.get('http://127.0.0.1:5000/list')
        print list.content


if __name__ == '__main__':
    unittest.main()
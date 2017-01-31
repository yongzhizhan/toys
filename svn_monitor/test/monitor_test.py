#!/usr/bin/eny python
#conding: utf-8

import unittest
from time import sleep
from unittest import TestCase

from database import DataBase
from models import SvnInfo, MailInfo
from svn_monitor import SvnMonitor


class MonitorTestCase(TestCase):
    def test_default(self):
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

        monitor = SvnMonitor(1)
        monitor.start()

        is_change = False
        for i in range(10):
            session.expire_all()
            info = session.query(SvnInfo).filter(SvnInfo.id == 0).first()
            if info.last_revision != 0:
                is_change = True
                break

            sleep(1)

        self.assertTrue(is_change)

        monitor.stop()
        return


if __name__ == '__main__':
    unittest.main()



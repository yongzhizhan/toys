#!/usr/bin/env python
# coding: utf-8


import unittest
from unittest import TestCase

from database import DataBase
import models


class DatabaseTestCase(TestCase):
    def test_get_session(self):
        db = DataBase("sqlite:///./data.db")
        db_session = db.get_session()

        db.init_db()

        svn_path = models.SvnInfo(path="123")
        db_session.add(svn_path)

        svn_path_query = db_session.query(models.SvnInfo).all()

        print svn_path_query

    def test_update(self):
        db = DataBase("sqlite:///./data.db")
        db_session = db.get_session()

        db.init_db()

        svn_path = models.SvnInfo(path="123")
        db_session.add(svn_path)
        db_session.commit()

        db_session.query(models.SvnInfo).filter(models.SvnInfo.path == "123").update({models.SvnInfo.path: "12345"})
        db_session.commit()

        svn_path_query = db_session.query(models.SvnInfo).all()

        for row in svn_path_query:
            print row.path

    def test_join(self):
        database = DataBase("sqlite:///./data.db")
        database.init_db()

        session = database.get_session()

        session.query(models.SvnInfo).delete()
        session.query(models.MailInfo).delete()
        session.commit()

        # add data
        svn_path = "http://10.10.8.23/repos/tmp/test"
        mail_address = "263435079@qq.com"

        svn_info = models.SvnInfo(0, svn_path, 0)
        session.add(svn_info)
        session.add(models.MailInfo(None, 0, mail_address))
        session.commit()

        list = session.query(models.SvnInfo, models.MailInfo).filter(models.SvnInfo.id == models.MailInfo.svn_id).all()
        for a, u in list:
            print a
            print u


if __name__ == "__main__":
    unittest.main()

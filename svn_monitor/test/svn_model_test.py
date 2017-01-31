#!/usr/bin/env python
# coding:utf-8

import unittest

import config
from svn_model import SvnModel


class SvnModelTest(unittest.TestCase):
    def test_default(self):
        try:
            svn_model = SvnModel("http://10.10.8.23/repos/tmp", config.svn_user, config.svn_pwd)
            revision = svn_model.get_revision()
            print revision
            if not revision:
                print "get resivion err"
                exit(-1)

            print "Revision is", revision

            print svn_model.get_logs()
        except Exception as e:
            print e

        return

if __name__ == '__main__':
    try:
        unittest.main()
    except Exception as e:
        print e

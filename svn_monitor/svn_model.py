#!/usr/bin/env python
# coding:utf-8

import subprocess
import xml.etree.cElementTree as ElementTree


class SvnModel:
    svn_path = ""
    username = ""
    password = ""

    def __init__(self, svnpath, username, password):
        self.svn_path = svnpath
        self.username = username
        self.password = password

    def get_svn_info(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if err:
            return None

        root = ElementTree.fromstring(output)
        return root

    def get_revision(self):
        cmd = "svn info {0} --username {1} --password {2} --xml".format(self.svn_path, self.username, self.password)
        root = self.get_svn_info(cmd)

        return root.getchildren()[0].attrib['revision']

    def get_logs(self, limit=10):
        cmd = "svn log {0} --username {1} --password {2} --limit {3} --xml".format(self.svn_path, self.username,
                                                                                   self.password, limit)

        root = self.get_svn_info(cmd)
        log_list = []
        for log_entry in root:
            log_list.append({
                "revision": log_entry.get("revision"),
                "author": log_entry.find("author").text,
                "msg": log_entry.find("msg").text,
                "date": log_entry.find("date").text
            })

        return log_list


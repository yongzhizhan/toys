#!/usr/bin/env python
# coding:utf-8

import threading
from time import sleep

from database import DataBase
from mail import Mail
from svn_model import SvnModel
from models import SvnInfo
from models import MailInfo
import config

class SvnMonitor:
    timer = None
    session = None
    stop_work = False
    intervalS = 3

    def __init__(self, intervalS):
        self.intervalS = intervalS

        database = DataBase("sqlite:///./data.db")
        database.init_db()

        self.session = database.get_session()
        self.timer = threading.Timer(0, self.run)

    def __del__(self):
        self.session.remove()

    def start(self):
        self.timer.start()

        return

    def stop(self):
        self.stop_work = True
        self.timer.cancel()


    def run(self):
        while not self.stop_work:
            self._run()
            sleep(self.intervalS)


    def _run(self):
        try:
            svn_infos = self.session.query(SvnInfo).all()
            for svn_info in svn_infos:
                path = svn_info.path

                svn_model = SvnModel(path, config.svn_user, config.svn_pwd)
                cur_revision = int(svn_model.get_revision())

                if svn_info.last_revision == cur_revision:
                    continue

                mail_addresses = self.session.query(MailInfo).filter(MailInfo.svn_id == svn_info.id).all()
                for mail_address in mail_addresses:
                    self.notify(svn_info, mail_address, cur_revision)

                #update
                self.session.query(SvnInfo).filter(SvnInfo.id == svn_info.id).update({SvnInfo.last_revision: cur_revision})
                self.session.commit()

        except Exception as e:
            self.session.rollback()
            print e

        return

    def notify(self, svn_info, mail_address, cur_revision):
        print "notify revision is " + str(cur_revision)

        mail = Mail(config.email_smtp, "svn monitor", "to " + mail_address, "new revision: " + str(cur_revision), svn_info.path + " updated current revision is: " + cur_revision)

        if config.email_use_ssl:
            mail.starttls()

        mail.login(config.email_user, config.email_pwd)
        mail.send(config.email_user, mail_address)

        return



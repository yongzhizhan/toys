#!/usr/bin/env python
# coding: utf-8


from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from database import Base


class SvnInfo(Base):
    __tablename__ = 'svn_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(255))
    last_revision = Column(Integer)

    def __init__(self, id = None, path = None, last_revision = None):
        self.path = path
        self.id = id
        self.last_revision = last_revision

    def __repr__(self):
        return "<path = %s, id = %d, last_revision = %d>" % (self.path, self.id, self.last_revision)

class MailInfo(Base):
    __tablename__ = 'mail_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    svn_id = Column(Integer)
    mail_address = Column(String(255))

    def __init__(self, id = None, svn_id = None, mail_address = None):
        self.svn_id = svn_id
        self.id = id
        self.mail_address = mail_address


    def __repr__(self):
        return "<svn_id = %d, id = %d, mail_address = %s>" % (self.svn_id, self.id, self.mail_address)


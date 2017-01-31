#!/usr/bin/env python
# coding: utf-8

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DataBase:
    engine = None
    session = None
    metadata = None

    def __init__(self, url):
        self.engine = create_engine(url)
        self.session = sessionmaker(autocommit=False , autoflush=False, bind=self.engine)()

        return

    def init_db(self):
        # noinspection PyUnresolvedReferences
        import models
        Base.metadata.create_all(bind=self.engine)
        return


    def get_session(self):
        return self.session

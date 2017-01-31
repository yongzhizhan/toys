#!/usr/bin/env python
# coding: utf-8


import unittest

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class SqlAlchemyTestCase(unittest.TestCase):
    def test_create_table(self):
        engine = create_engine("sqlite:///./db.db")
        metadata = MetaData()
        user_table = Table("users", metadata,
                           Column("Id", Integer, primary_key=True, autoincrement=True),
                           Column("Name", String(50))
                           )

        if False == user_table.exists(engine):
            user_table.create(bind=engine)

        conn = engine.connect()
        conn.execute(user_table.insert())

        Base = automap_base()
        Base.prepare(engine, reflect=True)

        Users = Base.classes.users

        session = Session(engine)
        session.add(Users(Name = "test"))
        session.commit()

        for row in session.query(Users).all():
            print row


if __name__ == "__main__":
    unittest.main()

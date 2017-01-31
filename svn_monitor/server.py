#!/usr/bin/env python
# coding:utf-8


from flask import Flask, request, render_template

import sqlite3
import json
import random

import config
from database import DataBase
from models import SvnInfo, MailInfo
from svn_monitor import SvnMonitor

app = Flask(__name__)

# database
database = DataBase("sqlite:///./data.db")
database.init_db()

session = database.get_session()


@app.route("/", methods=["GET"])
def index():
    randomVal = random.randint(0, 1000)
    return render_template("index.html", randomVal=randomVal)


@app.route("/add", methods=["POST"])
def add():
    jsonData = json.loads(request.data)
    svnPath = jsonData["svnPath"]
    mail = jsonData["mail"]

    try:
        svn_id = session.query(SvnInfo).filter(SvnInfo.path == svnPath).first().id
        session.add(MailInfo(None, svn_id, mail))
        session.commit()
    except Exception as e:
        session.rollback()
        print e
        return json.dumps({"success": False})

    return json.dumps({"success": True})


@app.route("/delete", methods=['POST'])
def delete():
    jsonData = json.loads(request.data)
    id = jsonData["id"]

    try:
        session.query(MailInfo).filter(MailInfo.id == id).delete()
        session.commit()
    except sqlite3.Error as e:
        session.rollback()
        print e
        return json.dumps({"success": False})

    return json.dumps({"success": True})


@app.route("/list", methods=["GET"])
def get_list():
    list = []

    try:
        info_list = session.query(MailInfo, SvnInfo).filter(SvnInfo.id == MailInfo.svn_id).all()
        for mail_info, svn_info in info_list:
            list.append({
                "id": mail_info.id,
                "svnpath": svn_info.path,
                "mail": mail_info.mail_address
            })

    except sqlite3.Error as e:
        print e
        return json.dumps({"success": False})

    return json.dumps({"success": True, "data": list})


@app.route("/list_svn", methods=["GET"])
def list_svn():
    list = []

    try:
        info_list = session.query(SvnInfo).all()
        for svn_info in info_list:
            list.append({
                "id": svn_info.id,
                "path": svn_info.path
            })

    except Exception as e:
        return json.dumps({"success": False})
        print e

    return json.dumps({"success": True, "data": list})


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def add_test_data():
    database = DataBase("sqlite:///./data.db")
    database.init_db()

    session = database.get_session()

    session.query(SvnInfo).delete()
    session.query(MailInfo).delete()
    session.commit()

    # add data
    svn_path = "http://10.10.8.23/repos/tmp/test"
    mail_address = "263435079@qq.com"

    session.add(SvnInfo(0, svn_path, 0))
    session.add(MailInfo(None, 0, mail_address))
    session.commit()


if __name__ == "__main__":
    add_test_data()

    monitor = SvnMonitor(config.intervalS)
    monitor.start()

    app.run()

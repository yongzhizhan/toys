#!/bin/bash

cd `dirname $0`

mkdir svn_monitor
rsync -rv --exclude=Docker ../* ./svn_monitor/
cp -f ../config.default.py ./svn_monitor/config.py


docker build -t yongzhizhan/svn_monitor .

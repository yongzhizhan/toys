FROM micktwomey/python2.7

# Define working directory.
WORKDIR /opt/svn_monitor


RUN pip install flask
RUN pip install sqlalchemy
  
RUN cp /etc/apt/sources.list /etc/apt/sources.list.bac

# 更换为163的源，国内你懂的
ADD ./sources.list /etc/apt/

RUN apt-get -qqy update
RUN apt-get -y install subversion

ADD ./svn_monitor /opt/svn_monitor

EXPOSE 5000
ENTRYPOINT ["/usr/bin/python2.7"]
CMD ["/opt/svn_monitor/server.py" ]


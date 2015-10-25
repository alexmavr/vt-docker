#!/bin/sh
sudo -E /usr/bin/python /home/ubuntu/collaborative-vistrails/vistrails/run.py -t $MYSQL_PORT_3306_TCP_ADDR -r 3306 -f vistrails -u root

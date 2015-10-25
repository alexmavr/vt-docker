import docker
from subprocess import call
import os
import signal
import sys

cwd = os.getcwd()

teams = int(raw_input("How many teams of 4 are there in the experiment? "))

c = docker.Client()

mysql_conts = []

def sigint_handler(signal, frame):
    for ctr in mysql_conts:
        c.remove_container(ctr.get("Id"))
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

for team in range(teams):
    teamid = "team"+str(team)
    print teamid

    # Launch MySQL container
    mysqlpath = teamid+"mysql"
    ctr = c.create_container(image="afein/mysql-vistrails", 
                             environment={"MYSQL_ROOT_PASSWORD": "root"},
                             name=mysqlpath)
    resp = c.start(container=ctr.get("Id"))
    mysql_conts.append(ctr)

    # Launch Git container
    gitpath = teamid+"git"
    new_ctr = c.create_container(image="afein/sshgit", 
                                 ports=[22],
                                 name=gitpath)
    git_ctr_id = new_ctr.get("Id")
    resp = c.start(container=git_ctr_id)
    

    
    for member in range(4):
        ctr = c.create_container(image="afein/vt-experiment", 
                                 ports=[6080],
                                 host_config=c.create_host_config(port_bindings={
                                     6080: ('0.0.0.0',)
                                 }, 
                                     links={mysqlpath:"mysql", gitpath:"git"}
                                 ))
        resp = c.start(container=ctr.get("Id"))
        print " Team " + str(team) + " Member " + str(member) + " port: " + c.port(ctr.get("Id"), 6080)[0]["HostPort"]


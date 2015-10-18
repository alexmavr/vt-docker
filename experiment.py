import docker
from subprocess import call
import os
import signal
import sys

cwd = os.getcwd()

teams = int(raw_input("How many teams of 4 are there in the experiment? "))

c = docker.Client()

# cleanup
os.system("sudo rm -rf team*")

mysql_conts = []

def sigint_handler(signal, frame):
    for ctr in mysql_conts:
        c.remove_container(ctr.get("Id"))
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

for team in range(teams):
    teamid = "team"+str(team)
    print teamid

    call(["cp", "-rf", "template", teamid])
    os.system("cd " + teamid + "&& git branch test && git checkout test")

    # Launch MySQL container
    mysqlpath = teamid+"mysql"
    ctr = c.create_container(image="mysql/mysql-server", 
                             environment={"MYSQL_ROOT_PASSWORD": "root"},
                             name=mysqlpath)
    resp = c.start(container=ctr.get("Id"))
    mysql_conts.append(ctr)

    
    for member in range(4):
        ctr = c.create_container(image="afein/vt-experiment", 
                                 ports=[22, 6080],
                                 volumes=["/opt/remotegit"],
                                 host_config=c.create_host_config(port_bindings={
                                     22: ('127.0.0.1',),
                                     6080: ('127.0.0.1',)
                                 }, binds = [cwd + "/" + teamid + ":/opt/remotegit"],
                                 links={mysqlpath:"mysql"}
                                 ))
        resp = c.start(container=ctr.get("Id"))

    #mkdir team repo
    # docker run 4 containers, mount repo
    # return port numbers


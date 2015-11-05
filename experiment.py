import docker
from subprocess import call
import os
import signal
import sys
import socket
import struct
import fcntl

cwd = os.getcwd()

teams = int(raw_input("How many teams of 4 are there in the experiment? "))

c = docker.Client()

mysql_conts = []

def sigint_handler(signal, frame):
    for ctr in mysql_conts:
        c.remove_container(ctr.get("Id"))
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

# IP Address retrieval for an interface
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

ip = get_ip_address('wlan0')  


# Launch Form Redirect container on port 80
ctr = c.create_container(image="afein/redirform", 
                         ports=[80],
                         host_config=c.create_host_config(port_bindings={
                             80: ('0.0.0.0', 80)
                         }))
resp = c.start(container=ctr.get("Id"))

for team in range(teams):
    teamid = "team"+str(team)
    print teamid
    os.system("rm -rf "+teamid)
    os.system("mkdir "+teamid)

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
                                 volumes=['/home/ubuntu/Desktop/Dropbox'],
                                 host_config=c.create_host_config(port_bindings={
                                     6080: ('0.0.0.0',)
                                 }, 
                                     binds=[cwd + "/" + teamid + ":/home/ubuntu/Desktop/Dropbox"],
                                     links={mysqlpath:"mysql", gitpath:"git"}
                                 ))
        resp = c.start(container=ctr.get("Id"))
        print " Team " + str(team) + " Member " + str(member) + " : http://" +ip +":"+ c.port(ctr.get("Id"), 6080)[0]["HostPort"]


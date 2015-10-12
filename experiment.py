import docker
from subprocess import call
import os

cwd = os.getcwd()
print cwd

teams = int(raw_input("How many teams of 4 are there in the experiment? "))

c = docker.Client()

for team in range(teams):
    teamid = "team"+str(team)
    call(["mkdir", teamid])
    call(["git", "init", teamid])
    print teamid
    
    for member in range(4):
        ctr = c.create_container(image="afein/vt-experiment", 
                                 ports=[22, 6080],
                                 volumes=["/opt/remotegit"],
                                 host_config=c.create_host_config(port_bindings={
                                     22: ('127.0.0.1',),
                                     6080: ('127.0.0.1',)
                                 }, binds = [cwd + "/" + teamid + ":/opt/remotegit"]
                                 ))
        resp = c.start(container=ctr.get("Id"))
        print resp

    #mkdir team repo
    # docker run 4 containers, mount repo
    # return port numbers


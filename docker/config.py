import os

def get_and_printenv():
    print os.environ
    return os.environ["GIT_PORT_22_TCP_ADDR"]

local_repository="/home/ubuntu/localgit"
remote_host=get_and_printenv()
remote_username="root"
remote_repository="/opt/remotegit"

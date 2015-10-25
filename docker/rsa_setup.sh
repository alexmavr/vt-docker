#!/bin/sh
ssh-keygen -t rsa
ssh-copy-id root@$GIT_PORT_22_TCP_ADDR

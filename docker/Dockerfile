FROM ubuntu:14.04.2
MAINTAINER Doro Wu <fcwu.tw@gmail.com>

ENV DEBIAN_FRONTEND noninteractive
ENV HOME /root

# Desktop packages
RUN apt-get update \
    && apt-get install -y --force-yes --no-install-recommends supervisor \
        pwgen sudo vim-tiny \
        net-tools \
        lxde x11vnc xvfb \
        gtk2-engines-murrine ttf-ubuntu-font-family \
        firefox \
        fonts-wqy-microhei \
        language-pack-zh-hant language-pack-gnome-zh-hant firefox-locale-zh-hant \
        nginx \
        python-pip python-dev build-essential \
    && apt-get autoclean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get install -y x11vnc x11vnc-data
ADD web /web/
RUN pip install -r /web/requirements.txt
ADD noVNC /noVNC/
ADD nginx.conf /etc/nginx/sites-enabled/default
ADD supervisord.conf /etc/supervisor/conf.d/


# Vistrails packages
RUN sudo apt-get update && sudo apt-get install -y python python-dev python-pip git xvfb python-qt4 python-qt4-gl python-qt4-sql python-vtk gfortran libopenblas-dev liblapack-dev zip
RUN sudo pip install numpy && sudo pip install scipy gitpython
RUN sudo apt-get install -y libxext-dev libxrender-dev libxtst-dev
RUN sudo apt-get install -y python-mysqldb python-matplotlib python-qscintilla2


# VisTrails layer
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/ubuntu/Desktop && \
    echo "ubuntu:x:${uid}:${gid}:ubuntu,,,:/home/ubuntu:/bin/bash" >> /etc/passwd && \
    echo "ubuntu:x:${uid}:" >> /etc/group && \
    echo "ubuntu ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/ubuntu && \
    chmod 0440 /etc/sudoers.d/ubuntu && \
    chown ${uid}:${gid} -R /home/ubuntu

RUN mkdir /home/ubuntu/.ssh
RUN chown 1000:1000 -R /home/ubuntu/.ssh
RUN echo "ubuntu:ubuntu" | chpasswd


ENV HOME /home/ubuntu
WORKDIR /home/ubuntu

RUN echo asasd
ADD startup.sh /home/ubuntu/startup.sh
ADD vistrails.sh /home/ubuntu/Desktop/
ADD rsa_setup.sh /home/ubuntu/
RUN mkdir /home/ubuntu/Desktop/Dropbox

RUN git clone https://github.com/cmusv-sc/collaborative-vistrails /home/ubuntu/collaborative-vistrails
RUN chown -R ubuntu /home/ubuntu/collaborative-vistrails
RUN chgrp -R ubuntu /home/ubuntu/collaborative-vistrails
RUN chmod 777 -R /home/ubuntu/collaborative-vistrails
ADD config.py /home/ubuntu/collaborative-vistrails/vistrails/packages/collaboration/config.py

RUN sudo git config --global user.email "team@cmu.edu"
RUN sudo git config --global user.name "Team Member"

EXPOSE 6080
ENTRYPOINT ["/home/ubuntu/startup.sh"]

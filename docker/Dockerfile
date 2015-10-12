FROM ubuntu:14.04.2
MAINTAINER Doro Wu <fcwu.tw@gmail.com>

ENV DEBIAN_FRONTEND noninteractive
ENV HOME /root

# Desktop packages
RUN apt-get update \
    && apt-get install -y --force-yes --no-install-recommends supervisor \
        openssh-server pwgen sudo vim-tiny \
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
ADD startup.sh /
ADD supervisord.conf /etc/supervisor/conf.d/

# SSH setup
RUN mkdir /var/run/sshd
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
EXPOSE 22


# Vistrails packages
RUN sudo apt-get update && sudo apt-get install -y python python-dev python-pip git xvfb python-qt4 python-qt4-gl python-qt4-sql python-vtk gfortran libopenblas-dev liblapack-dev zip
RUN sudo pip install numpy && sudo pip install scipy gitpython
RUN sudo apt-get install -y libxext-dev libxrender-dev libxtst-dev


# VisTrails layer
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/ubuntu/Desktop && \
    echo "ubuntu:x:${uid}:${gid}:ubuntu,,,:/home/ubuntu:/bin/bash" >> /etc/passwd && \
    echo "ubuntu:x:${uid}:" >> /etc/group && \
    echo "ubuntu ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/ubuntu && \
    chmod 0440 /etc/sudoers.d/ubuntu && \
    chown ${uid}:${gid} -R /home/ubuntu

ENV HOME /home/ubuntu
WORKDIR /home/ubuntu

RUN git clone https://github.com/cmusv-sc/collaborative-vistrails


ADD config.py /home/ubuntu/collaborative-vistrails/vistrails/packages/collaboration/config.py

ADD vistrails.sh /home/ubuntu/Desktop/
ADD startup.sh /home/ubuntu/startup.sh
RUN /home/ubuntu/startup.sh

EXPOSE 6080
ENTRYPOINT ["/usr/bin/python /home/ubuntu/collaborative-vistrails/vistrails/run.py"]

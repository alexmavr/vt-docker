FROM ubuntu:14.04

RUN sudo apt-get update && sudo apt-get install -y python python-dev python-pip git xvfb python-qt4 python-qt4-gl python-qt4-sql python-vtk gfortran libopenblas-dev liblapack-dev zip
RUN sudo pip install numpy && sudo pip install scipy gitpython
RUN sudo apt-get install -y libxext-dev libxrender-dev libxtst-dev

RUN export uid=1000 gid=1000 && \
    mkdir -p /home/developer && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown ${uid}:${gid} -R /home/developer

USER developer
ENV HOME /home/developer
WORKDIR /home/developer
RUN git clone https://github.com/cmusv-sc/collaborative-vistrails


RUN git init /home/developer/localgit
ADD config.py /home/developer/collaborative-vistrails/vistrails/packages/collaboration/config.py
RUN cat /home/developer/collaborative-vistrails/vistrails/packages/collaboration/config.py

CMD python /home/developer/collaborative-vistrails/vistrails/run.py

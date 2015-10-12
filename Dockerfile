FROM afein/ubuntuvnc:latest

RUN sudo apt-get update && sudo apt-get install -y python python-dev python-pip git xvfb python-qt4 python-qt4-gl python-qt4-sql python-vtk gfortran libopenblas-dev liblapack-dev zip
RUN sudo pip install numpy && sudo pip install scipy gitpython
RUN sudo apt-get install -y libxext-dev libxrender-dev libxtst-dev

RUN export uid=1000 gid=1000 && \
    mkdir -p /home/ubuntu && \
    echo "ubuntu:x:${uid}:${gid}:ubuntu,,,:/home/ubuntu:/bin/bash" >> /etc/passwd && \
    echo "ubuntu:x:${uid}:" >> /etc/group && \
    echo "ubuntu ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/ubuntu && \
    chmod 0440 /etc/sudoers.d/ubuntu && \
    chown ${uid}:${gid} -R /home/ubuntu

USER ubuntu
ENV HOME /home/ubuntu
WORKDIR /home/ubuntu
RUN git clone https://github.com/cmusv-sc/collaborative-vistrails

ADD config.py /home/ubuntu/collaborative-vistrails/vistrails/packages/collaboration/config.py

CMD python /home/ubuntu/collaborative-vistrails/vistrails/run.py

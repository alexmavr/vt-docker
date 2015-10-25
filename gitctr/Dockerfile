FROM ubuntu:14.04.2

ENV DEBIAN_FRONTEND noninteractive
ENV HOME /root

# Desktop packages
RUN apt-get update \
    && apt-get install -y --force-yes --no-install-recommends git\
        openssh-server pwgen sudo vim-tiny \
        net-tools \
        fonts-wqy-microhei \
        python-pip python-dev build-essential \
    && apt-get autoclean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

# SSH setup
RUN mkdir /var/run/sshd
RUN echo "root:screencast" | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" > /etc/profile
EXPOSE 22

RUN ssh-keygen -f id_rsa -t rsa -N ''
RUN mkdir /root/.ssh
RUN cat id_rsa.pub > /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys
RUN mv id_rsa /root/.ssh


ADD template /opt/remotegit

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]

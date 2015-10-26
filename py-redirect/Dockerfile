FROM ubuntu
RUN sudo apt-get update && sudo apt-get install -y python

RUN echo there
ADD redir.py /redir.py

EXPOSE 80

ENTRYPOINT ["python", "/redir.py"]

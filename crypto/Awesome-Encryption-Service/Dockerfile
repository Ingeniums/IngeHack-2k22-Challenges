FROM golang:latest 

USER root

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends openssh-server socat


RUN useradd -ms /bin/bash  chall

USER chall 

RUN mkdir /home/chall/challenge

COPY challenge /home/chall/challenge

WORKDIR /home/chall/challenge

EXPOSE 1337


ENTRYPOINT sh entrypoint.sh

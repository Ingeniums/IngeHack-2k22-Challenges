FROM sagemath/sagemath:9.1

USER root

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends openssh-server socat


USER sage

RUN mkdir /home/sage/challenge

COPY challenge /home/sage/challenge

WORKDIR /home/sage/challenge

EXPOSE 1337


ENTRYPOINT sh entrypoint.sh

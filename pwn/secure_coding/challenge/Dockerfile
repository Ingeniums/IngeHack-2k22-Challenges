FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y socat && \ 
    rm -rf /var/lib/apt/lists/*

RUN useradd coding 
WORKDIR /home/coding 

COPY flag.txt /home/coding/flag.txt
COPY chall /home/coding/chall
COPY entrypoint.sh /home/coding/entrypoint.sh
COPY libc.so.6 /home/coding/libc.so.6
COPY ld-2.31.so /home/coding/ld-2.31.so

RUN chmod +x chall entrypoint.sh ld-2.31.so libc.so.6 && chown coding:coding .


EXPOSE 9001

USER coding 

CMD ["./entrypoint.sh"]

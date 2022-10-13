FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y socat patchelf && \ 
    rm -rf /var/lib/apt/lists/*

RUN useradd game 
WORKDIR /home/game 

COPY flag.txt ./ 
COPY chall ./
COPY libc.so.6 ./
COPY ld-2.29.so ./
COPY entrypoint.sh ./

RUN patchelf --set-interpreter ./ld-2.29.so --replace-needed libc.so.6 ./libc.so.6 chall
RUN chmod +x chall entrypoint.sh libc.so.6 ld-2.29.so && chown game:game . 

USER game 

CMD ["./entrypoint.sh"]

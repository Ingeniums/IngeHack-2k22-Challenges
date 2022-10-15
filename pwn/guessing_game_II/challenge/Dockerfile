FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y socat  && \ 
    rm -rf /var/lib/apt/lists/*

RUN useradd game_2 
WORKDIR /home/game_2 

COPY flag.txt ./ 
COPY chall ./
COPY entrypoint.sh ./

RUN chmod +x chall entrypoint.sh && chown game_2:game_2 . 
RUN ls -l
EXPOSE 9006

USER game_2 

CMD ["./entrypoint.sh"]
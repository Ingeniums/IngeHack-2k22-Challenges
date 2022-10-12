FROM python

RUN apt-get update && apt-get upgrade \
    && apt-get install -y socat \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /home/ingehack/challenge
COPY ./challenge/main.py .
RUN chmod +x main.py
EXPOSE 9999
CMD socat -dd -T300 TCP-L:9999,reuseaddr,fork,su="nobody" EXEC:"python main.py",stderr
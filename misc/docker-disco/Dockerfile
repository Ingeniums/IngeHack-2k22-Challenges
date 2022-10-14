FROM scorpion197/docker-disco:latest

WORKDIR /home/challenge/
COPY ./app/main.py ./main.py  
COPY ./app/Dockerfile ./Dockerfile

RUN ls -l 
RUN ls /home/challenge
EXPOSE 5000 

CMD ["python3", "main.py"]

FROM python

RUN pip install quart
COPY ./app /home/ingehack/app
WORKDIR /home/ingehack/app

EXPOSE 5000

CMD ["python", "main.py"]

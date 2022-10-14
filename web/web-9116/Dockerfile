FROM python

RUN pip install fastapi uvicorn
RUN useradd -ms /bin/bash  ingehack
COPY ./app /home/ingehack/app
RUN chown -R ingehack:root /home/ingehack/app

USER ingehack
WORKDIR /home/ingehack/app
EXPOSE 5000
CMD ["python", "main.py"]

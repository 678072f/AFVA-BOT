# Dockerfile, Image, Container

FROM python:3.10

ADD main.py .

ADD botCommands.py .

RUN pip3 install requests discord schedule python-dotenv

CMD [ "doppler run -- python3", "./main.py"]
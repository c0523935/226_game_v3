FROM python:3.11

RUN mkdir /server

COPY *.py /server/

CMD [ "python3.11", "/server/main.py" ]


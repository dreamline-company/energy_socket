# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /server/

COPY requirements.txt /server/requirements.txt
RUN pip3 install -r /server/requirements.txt

COPY socket_data_parser.py /server/
COPY logging.conf /server/
COPY server.py /server/
COPY .env /server/
COPY /service /server/service
COPY /database /server/database
EXPOSE 8070

CMD ["python3", "-u", "/server/server.py"]

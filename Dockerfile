# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /server/

COPY requirements.txt /server/requirements.txt
RUN pip3 install -r /server/requirements.txt

COPY . /server

EXPOSE 8070

CMD ["python3", "/server/server.py"]
FROM python:latest
WORKDIR /
COPY ./src/ .
RUN pip install mysql-connector-python
CMD ["python3", "./src/uptime_downtime.py"]
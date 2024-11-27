FROM python:latest
WORKDIR /
COPY ./src/ .
RUN pip install mysql-connector-python
CMD ["python", "./uptime_downtime.py"]
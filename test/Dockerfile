FROM python:3.11

RUN pip install locust

WORKDIR /mnt/locust

COPY locustfile.py .

EXPOSE 8089

CMD ["locust", "-f", "/mnt/locust/locustfile.py", "--host=http://backend:8000"]
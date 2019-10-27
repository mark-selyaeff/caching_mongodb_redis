FROM python:3.7-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY cache-server.py cache-server.py
CMD ["python", "cache-server.py"]
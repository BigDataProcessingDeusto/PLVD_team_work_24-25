FROM python:3.10-slim

WORKDIR /app

RUN pip install kafka-python faker

COPY produce_events.py .

CMD ["python", "produce_events.py"]

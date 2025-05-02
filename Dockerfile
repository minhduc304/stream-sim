FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml /app/
COPY README.md /app/

# Install the package in development mode
RUN pip install --no-cache-dir -e .

# Install optional dependencies
RUN pip install --no-cache-dir faker kafka-python 

# Copy application code
COPY data_stream_simulator/ /app/data_stream_simulator/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command
ENTRYPOINT ["python", "-m", "data_stream_simulator"]
CMD ["--config", "/app/config.yaml"]

version: '3'

services:
  simulator:
    build: .
    volumes:
      - ./examples:/app/examples
      - ./output:/app/output
    command: --config /app/examples/sensor_data.yaml
    environment:
      - PYTHONUNBUFFERED=1
    networks:
      - simulator-network

  # Optional services for testing
  kafka:
    image: bitnami/kafka:latest
    ports:
      - "9092:9092"
    environment:
      - KAFKA_CFG_NODE_ID=0
      - KAFKA_CFG_PROCESS_ROLES=controller,broker
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_INTER_BROKER_LISTENER_NAME=PLAINTEXT
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka:9093
      - ALLOW_PLAINTEXT_LISTENER=yes
    networks:
      - simulator-network

  mqtt:
    image: eclipse-mosquitto:latest
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log
    networks:
      - simulator-network

networks:
  simulator-network:
    driver: bridge
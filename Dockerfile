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


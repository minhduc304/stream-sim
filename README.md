# Data Stream Simulator

A configurable real-time data streaming simulator capable of generating realistic data streams for testing and development purposes.

## Features

- **Schema-based Data Generation**: Define your data structure and generate realistic values
- **Multiple Output Formats**: Generate JSON, CSV and other formats
- **Multiple Destinations**: Stream to files, stdout, Kafka, HTTP endpoints etc.
- **Time Control**: Configure the rate of data generation and optional jitter
- **Event Injection**: Insert predefined anomalies or events into the stream
- **Stateful Generation**: Support for maintaining state between records
- **Docker Ready**: Easy containerization for deployment

## Installation

### From Source

```bash
git clone https://github.com/minhduc304/stream-sim.git
cd data-stream-simulator
pip install -e .
```

For all optional dependencies:

```bash
pip install -e ".[all]"
```

### With Docker

```bash
git clone https://github.com/yourusername/data-stream-simulator.git
cd data-stream-simulator
docker build -t data-stream-simulator .
```

## Quick Start

1. Create a configuration file (YAML):

```yaml
streams:
  sensor:
    schema:
      id:
        type: uuid
      timestamp:
        type: timestamp
        format: iso
      temperature:
        type: random_float
        min: 20.0
        max: 30.0
        precision: 1
      humidity:
        type: random_int
        min: 40
        max: 90
    rate: 1  # records per second
    outputs:
      - type: stdout
        format: json
```

2. Run the simulator:

```bash
data-stream-simulator --config your_config.yaml
```

Or with Docker:

```bash
docker run -v $(pwd)/your_config.yaml:/app/config.yaml data-stream-simulator
```

## Configuration Reference

### Top-Level Structure

```yaml
streams:
  stream_name_1:
    # Stream 1 configuration
  stream_name_2:
    # Stream 2 configuration
```

### Stream Configuration

```yaml
schema:
  # Record schema definition
rate: 1.0  # Records per second
jitter: 0.1  # Optional: Random variation in timing (0.1 = ±10%)
initial_state:  # Optional: Initial state values
  counter: 0
events:  # Optional: Event definitions
  - record:  # Event record to inject
      temperature: 100.0
      status: "ALERT"
    at_count: 10  # Trigger at 10th record
  - record:
      status: "WARNING"
    probability: 0.05  # 5% chance per record
outputs:
  - type: stdout  # Output type
    format: json  # Output format
  - type: file
    format: csv
    filename: "output/data.csv"
```

### Data Generation Types

The simulator supports various types of data generators:

- `static`: Fixed value
- `random_int`: Random integer within range
- `random_float`: Random float within range
- `sequence_int`: Integer sequence
- `choice`: Random selection from a list
- `timestamp`: Current time in various formats
- `uuid`: Generate a UUID
- `gaussian`: Value from normal distribution
- `faker`: Realistic fake data using Faker library
- `dependent`: Value depends on another field
- `stateful`: State-dependent generation

Example schema with different generators:

```yaml
schema:
  device_id:
    type: static
    value: "sensor-001"
  sequence:
    type: sequence_int
    start: 1
    step: 1
  value:
    type: random_float
    min: 0.0
    max: 100.0
    precision: 2
  status:
    type: choice
    values: ["OK", "WARNING", "ERROR"]
    weights: [0.8, 0.15, 0.05]
  created_at:
    type: timestamp
    format: iso
  location:
    type: faker
    type: address
```

### Output Types

- `stdout`: Console output
- `file`: Write to a file
- `kafka`: Send to Kafka topic
- `http`: Send to HTTP endpoint
- `mqtt`: Publish to MQTT topic

## Docker Compose

For complex testing scenarios, use docker-compose:

```bash
docker-compose up
```

This will start the simulator and supporting services (Kafka, MQTT) as defined in the docker-compose.yml file.

## Examples

Check the `examples/` directory for sample configurations:

- `stock_market.yaml`: Stock price updates
- `web_traffic.yaml`: Web server logs simulation

## License

MIT
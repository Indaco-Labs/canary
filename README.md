
# Canary

Canary is an environmental monitoring system developed by **Indaco Labs**. It is designed to collect temperature and humidity readings from four DHT22 sensor modules connected to a Raspberry Pi 4.

## Status

The project is in its initial development stage. This repository currently contains the Python packaging foundation only; sensor acquisition, persistence, alerts and the web API are not yet implemented.

## Planned architecture

- Python 3.12 application with a `src/` package layout
- Hardware-independent sensor interfaces and simulated sensors for testing
- Independent data acquisition service
- SQLite storage for timestamped measurements
- FastAPI REST API and browser-based dashboard
- Automated testing with pytest and CI using GitHub Actions

## Development setup

Use Python 3.12 and create a virtual environment in the repository root:

```bash
python3 -m venv .venv
```

Activate it on Linux:

```bash
source .venv/bin/activate
```

Install the package and development tools in editable mode:

```bash
python -m pip install -e '.[dev]'
```

Verify the installation:

```bash
python -c "import canary; print(canary.__file__)"
python -m ruff check .
python -m mypy
```



## Hardware plan

| Sensor | BCM GPIO | Raspberry Pi physical pin |
| --- | --- | --- |
| sensor-01 | GPIO4 | 7 |
| sensor-02 | GPIO17 | 11 |
| sensor-03 | GPIO27 | 13 |
| sensor-04 | GPIO22 | 15 |

The DHT22 modules share 3.3 V and ground. Physical sensor access is not required for initial development.

## Licence

A licence has not yet been selected. 
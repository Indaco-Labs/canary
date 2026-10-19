# 001. Adopt the Core Technology Stack

* **Status:** Accepted
* **Date:** 2026-10-19
* **Deciders:** Indaco Labs — Canary Project Manager

## Context

Canary requires a software stack capable of acquiring temperature and humidity measurements from four DHT22 sensors connected to a Raspberry Pi 4.

The application must:

* Acquire measurements at 60-second intervals.
* Store timestamped historical measurements.
* Expose measurement history through a web interface.
* Display temperature and humidity charts.
* Support configurable per-sensor thresholds.
* Display active and historical alerts locally.
* Support automated unit and integration testing without physical hardware.
* Operate on a Raspberry Pi without paid cloud infrastructure.

The project should favour maintainability, low resource consumption, hardware abstraction and a development environment that works on both Linux laptops and Raspberry Pi OS.

## Options Considered

* **Option 1: Python, FastAPI, Chart.js and SQLite** — Pros: Mature Python ecosystem, strong automated testing support, lightweight database, typed API framework and a customisable browser interface. Cons: Requires developing and maintaining dashboard components and managing separate acquisition and API processes.
* **Option 2: Python with Grafana and a time-series database** — Pros: Mature dashboards, advanced visualisation and established monitoring capabilities. Cons: Additional services, configuration complexity and potentially greater resource consumption for a small four-sensor system.
* **Option 3: Node.js with a JavaScript frontend and database** — Pros: Common language across frontend and backend, mature web tooling and extensive package ecosystem. Cons: Less direct alignment with the selected Python hardware and testing ecosystem.

## Decision

We chose **Python, FastAPI, Chart.js and SQLite** as the core technology stack because this combination supports the required functionality while remaining lightweight, testable and suitable for Raspberry Pi deployment.

The architecture will use the following technologies:

**Primary language**

* Python 3, using a currently supported version compatible with the selected Raspberry Pi OS and DHT22 driver.

**Backend framework**

* FastAPI for REST API endpoints, configuration management and serving the web interface.
* Pydantic for configuration and data validation.

**Frontend**

* HTML, CSS and JavaScript.
* Chart.js for temperature and humidity visualisation.
* A responsive, locally hosted dashboard without a separate frontend application framework.

**Database**

* SQLite for persistent measurements, sensor configuration, thresholds and alert history.
* Schema migrations will be version-controlled.
* SQLite Write-Ahead Logging will be evaluated and enabled where appropriate for concurrent application access.

**Hardware integration**

* A Python DHT22 adapter using a compatible Raspberry Pi GPIO library.
* Hardware access will be isolated behind a sensor interface.
* A simulated sensor adapter will support development and testing without physical hardware.
* The specific GPIO driver will be selected after compatibility testing on the target Raspberry Pi OS.

**Acquisition**

* A dedicated Python acquisition process operating on a 60-second sampling interval.
* Each sensor will be independently identifiable.
* Failed measurements will not be represented as valid sensor readings.
* Acquisition will continue independently of the web dashboard.

**Alerting**

* Per-sensor configurable upper and lower temperature and humidity thresholds.
* Persistent alert state and event history.
* Alerts displayed locally through the dashboard.
* No email, SMS, push or external notification service in the MVP.

**Testing**

* pytest for unit, integration and hardware-in-the-loop tests.
* Mocked or simulated sensor inputs for deterministic tests.
* GitHub Actions for automated checks.

**Runtime environment**

* Raspberry Pi 4 running a supported 64-bit Raspberry Pi OS release.
* Python virtual environments for dependency isolation.
* Development performed on a Linux laptop.
* Production services managed through systemd.

The exact Python version, GPIO library and dependency versions will be recorded after the hardware compatibility spike.

## Consequences

* **Positive:** Python provides a consistent language for acquisition, business logic, API development and automated testing.
* **Positive:** FastAPI supports clear API contracts and input validation.
* **Positive:** Chart.js enables a purpose-built dashboard without the overhead of a separate monitoring platform.
* **Positive:** SQLite avoids the operational complexity of a separate database server.
* **Positive:** Hardware abstraction enables extensive testing on development machines and GitHub-hosted CI runners.
* **Negative:** Dashboard components, alert presentation and configuration interfaces must be developed and maintained.
* **Negative:** SQLite is less suitable for high-volume distributed deployments, potentially requiring migration if the system expands significantly.
* **Negative:** GPIO library compatibility may depend on the Raspberry Pi OS and Python versions.
* **Negative:** The acquisition service and API require coordinated access to persistent storage.
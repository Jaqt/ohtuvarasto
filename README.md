# ohtuvarasto

[![GHA Workflow badge](https://github.com/Jaqt/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/Jaqt/ohtuvarasto/actions)
[![codecov](https://codecov.io/github/Jaqt/ohtuvarasto/graph/badge.svg?token=O7L9TQET0A)](https://codecov.io/github/Jaqt/ohtuvarasto)

A warehouse management application with both CLI and web interfaces.

## Features

- **Core Warehouse Class**: Manage warehouse inventory with capacity limits
- **Web Interface**: Flask-based web UI for managing multiple warehouses
- **CLI Demo**: Command-line demonstration of warehouse operations

## Installation

```bash
poetry install
```

## Running the Web Application

```bash
cd src
poetry run flask --app app run
```

Then open your browser to `http://127.0.0.1:5000`

### Web UI Features

- Create multiple warehouses with custom names and capacities
- Add and remove items from warehouses
- View real-time inventory levels and available space
- Delete warehouses when no longer needed

## Running Tests

```bash
poetry run pytest
```

## Development

Run linting:
```bash
poetry run pylint src/
```

Run with coverage:
```bash
poetry run coverage run --branch -m pytest src
poetry run coverage report -m
```

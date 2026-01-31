# Project Name

## Prerequisites

- Docker & Docker Compose
- uv (Python package manager)

## Quick Start
```bash
# Start the project
make up

# Run tests
make test

# Stop the project
make down
```

## Available Commands
```bash
make help    # Show all available commands
make up      # Start project with database seeding
make test    # Run tests
make down    # Stop all containers
make clean   # Stop containers and remove volumes
make logs    # Show all logs
make logs-db # Show database logs
make logs-api# Show API logs
```

## Development

After starting the project with `make up`, the API will be available at:
- http://localhost:8000

## Testing

Tests use a separate database instance. Run with:
```bash
make test
```
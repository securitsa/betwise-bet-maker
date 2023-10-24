# Betwise Bet Maker Service

## Overview

Cutting-edge platform that enables users to place bets and wagers with ease.

## Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL

## Installation and Setup

### Prerequisites

Before you can run the Bilinz User Management Service, ensure that you have the following prerequisites installed:

- Docker
- Docker Compose

### Getting Started

1. Clone the repository to your local machine.

```bash
git clone git@github.com:securitsa/betwise-line-provider.git
cd betwise-line-provider
```

2. Build and start the application using Docker Compose.
```bash
docker network create btw-dev-network`
```
```bash
make up-build
```

This command will set up the PostgreSQL database, apply migrations, and start the FastAPI application.

## Database Migrations

To manage database migrations, you can use the provided Makefile commands:

### Create a Migration

To create a new database migration, use the following command:

```bash
make create-migrations m="your_migration_name"
```

### Upgrade Migrations

To apply all pending database migrations, use the following command:

```bash
make migrations-upgrade
```

### Downgrade Migrations

To revert the last applied database migration, use the following command:

```bash
make migrations-downgrade
```

## Running the Service

To start the service, use the following command:

```bash
make up
```

This will run the FastAPI application inside a Docker container.

## Stopping the Service

To stop the service and remove the containers, use the following command:

```bash
make down
```

## Postman Tests

The project includes Postman tests for end-to-end testing of the API. To run these tests, use the following command:

```bash
make postman-tests
```

This command will execute the Postman tests using a Postman Docker container and the specified test environment.

## Folder Permissions (For Development)

If you encounter permission issues during development, you can use the following command to adjust folder permissions:

```bash
make chmod-versions
```

## Removing Volumes

To stop the service and remove associated volumes (e.g., database data), use the following command:

```bash
make down-remove-volumes
```

This will completely clean up the environment, including data stored in the database.

## API Documentation

Once the service is running, you can access the API documentation at `http://localhost:8062/docs` to explore and interact with the available endpoints.

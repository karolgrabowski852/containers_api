# containers-api

REST API for managing user containers using FastAPI, MongoDB, and Nginx as a reverse proxy.

## Documentation

- [API Endpoints](README/ENDPOINTS.md)
- [MongoDB Schema](README/MONGODB_SCHEMA.md)

## Requirements

- Docker
- Docker Compose

## Setup & Run

1. Configure the `.env` file based on `.env.example`:

```bash
cp .env.example .env

```

2. Start the application:

```bash
docker compose up --build
```

The API will be available at: [localhost:8000](http://localhost:8000)



## Endpoints

- `/users/` - user management
- `/containers/` - container management
- `/resources` - view available resources

## Author

Karol Grabowski

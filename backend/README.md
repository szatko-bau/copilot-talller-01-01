# Backend — JWT Authentication API

A minimal **FastAPI** application that demonstrates JWT-based authentication using
**access tokens** and **refresh tokens**. Dependencies are managed with **Poetry** and
the service can be deployed with **Docker / Docker Compose**.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Endpoints](#endpoints)
- [Local Development](#local-development)
- [Running with Docker](#running-with-docker)
- [Running with Docker Compose](#running-with-docker-compose)
- [Configuration](#configuration)
- [Running Tests](#running-tests)

---

## Architecture Overview

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI application and route handlers
│   └── auth.py        # JWT creation, verification and password hashing
├── tests/
│   └── test_api.py    # pytest test suite
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml     # Poetry dependency manifest
└── README.md
```

The application uses **HS256** signed JWTs via [`python-jose`](https://github.com/mpdavis/python-jose)
and bcrypt password hashing via [`passlib`](https://passlib.readthedocs.io/).

| Token type    | Lifetime  |
|---------------|-----------|
| Access token  | 300 s     |
| Refresh token | 24 h      |

---

## Endpoints

### `POST /token` — Login

Authenticate with username and password to receive a token pair.

**Request** (`application/x-www-form-urlencoded`):

| Field      | Value      |
|------------|------------|
| `username` | `admin`    |
| `password` | `admin123` |

**Response** (`200 OK`):

```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

**Example**:

```bash
curl -X POST http://localhost:8000/token \
  -d "username=admin&password=admin123"
```

---

### `POST /token/refresh` — Refresh tokens

Exchange a valid refresh token for a new token pair.

**Request** (`application/json`):

```json
{ "refresh_token": "<jwt>" }
```

**Response** (`200 OK`): same schema as `/token`.

**Example**:

```bash
curl -X POST http://localhost:8000/token/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<your_refresh_token>"}'
```

---

### `GET /me` — Current user (protected)

Returns the username of the authenticated user. Requires a valid access token.

**Request headers**:

```
Authorization: Bearer <access_token>
```

**Response** (`200 OK`):

```json
{ "username": "admin" }
```

**Example**:

```bash
curl http://localhost:8000/me \
  -H "Authorization: Bearer <your_access_token>"
```

---

### Interactive docs

FastAPI automatically generates interactive API documentation:

| URL                              | Tool     |
|----------------------------------|----------|
| `http://localhost:8000/docs`     | Swagger  |
| `http://localhost:8000/redoc`    | ReDoc    |

---

## Local Development

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)

### Install dependencies

```bash
cd backend
poetry install
```

### Start the development server

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## Running with Docker

```bash
cd backend

# Build the image
docker build -t jwt-backend .

# Run the container
docker run -p 8000:8000 \
  -e SECRET_KEY="your-super-secret-key" \
  jwt-backend
```

---

## Running with Docker Compose

```bash
cd backend
docker compose up --build
```

To run in the background:

```bash
docker compose up --build -d
```

To stop:

```bash
docker compose down
```

---

## Configuration

The following environment variable can be overridden:

| Variable     | Default                                           | Description                   |
|--------------|---------------------------------------------------|-------------------------------|
| `SECRET_KEY` | `change-me-in-production-use-a-long-random-string`| HS256 signing key for JWTs    |

> ⚠️ **Always** set a strong, random `SECRET_KEY` in production environments.

---

## Running Tests

```bash
cd backend
poetry run pytest tests/ -v
```

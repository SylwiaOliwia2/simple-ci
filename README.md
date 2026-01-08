# Distance Converter API

A simple FastAPI application that converts kilometers to miles. The API is containerized using Docker for easy deployment and usage.

## Features

- Convert kilometers to miles via a REST API endpoint
- Interactive API documentation (Swagger UI)
- Dockerized for easy deployment

## Prerequisites

- Docker installed on your system
  - [Install Docker](https://docs.docker.com/get-docker/)

## Building the Docker Image

To build the Docker image, run the following command in the project directory:

```bash
docker build -t simple-api .
```

This will create a Docker image named `simple-api`.

## Running the API

Once the image is built, you can run the container with:

```bash
docker run -p 8000:8000 simple-api
```

The `-p 8000:8000` flag maps port 8000 from the container to port 8000 on your host machine.

The API will be available at `http://localhost:8000`.

## API Endpoints

All the endpoints are listed in **Swagger UI:** http://localhost:8000/docs

### Convert Kilometers to Miles

- **URL:** `GET /convert`
- **Description:** Converts kilometers to miles
- **Query Parameters:**
  - `km` (float, required): Distance in kilometers

**Example Request:**
```bash
curl "http://localhost:8000/convert?km=10"
```

**Example Response:**
```json
{
  "kilometers": 10,
  "miles": 6.2137
}
```

## Conversion Formula

The API uses the standard conversion factor:
- **1 kilometer = 0.621371 miles**

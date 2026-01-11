# Distance Converter API

A simple FastAPI application that converts kilometers to miles. The API is containerized using Docker for easy deployment and usage.

## Features

- Convert kilometers to miles via a REST API endpoint
- Interactive API documentation (Swagger UI)
- Dockerized for easy deployment

## Prerequisites

- Docker installed on your system
  - [Install Docker](https://docs.docker.com/get-docker/)
- For Kubernetes deployment:
  - [kubectl](https://kubernetes.io/docs/tasks/tools/) installed
  - [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed

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

## Running Tests

To run the unit tests using Docker:

1. Build the Docker image (if not already built):
   ```bash
   docker build -t simple-api .
   ```

2. Run the tests:
   ```bash
   docker run --rm simple-api pytest tests/test_main.py -v
   ```

## CI

CI (Github Actions) is triggered:
- on every commit on `main` branch
- on every merge request to `main`


## Kubernetes Deployment

### Prerequisites

Ensure Minikube is running:
```bash
minikube start
minikube status
```

### Build and Load Docker Image

1. Unset minikube-docker environment (to use local Docker):
   ```bash
   eval $(minikube docker-env -u)
   ```

2. Build image in local Docker:
   ```bash
   docker build -t simple-api:latest .
   ```

3. Load image into Minikube:
   ```bash
   minikube image load simple-api:latest
   ```
   > **Note:** We load the image instead of building it directly in Minikube to avoid certificate permission errors.

4. Verify image is loaded:
   ```bash
   minikube image ls | grep simple-api
   ```

### Deploy to Kubernetes

1. Deploy the deployment:
   ```bash
   kubectl apply -f k8s/deployment.yaml
   ```

2. Check deployment status:
   ```bash
   kubectl get deployments
   kubectl get pods -l app=simple-api
   ```

3. Access the API locally using port-forward:
   
   **Option A: Port-forward to a pod directly:**
   ```bash
   # Get the pod name first
   kubectl get pods -l app=simple-api
   # Then port-forward (replace POD_NAME with actual pod name)
   kubectl port-forward pod/POD_NAME 8000:8000
   ```
   
   **Option B: Port-forward via Service (if service.yaml exists):**
   ```bash
   kubectl apply -f k8s/service.yaml
   kubectl port-forward service/simple-api 8000:80
   ```

4. In another terminal, test the API:
   ```bash
   curl "http://localhost:8000/convert?km=10"
   curl "http://localhost:8000/health"
   curl "http://localhost:8000/ready"
   ```

5. Access Swagger UI:
   Open http://localhost:8000/docs in your browser

### Rolling Updates

When you make changes to the code (e.g., `main.py`), you need to rebuild the Docker image and trigger a rolling update:

1. **Build the new Docker image:**
   ```bash
   # Make sure you're using local Docker
   eval $(minikube docker-env -u)
   
   # Build the updated image
   docker build -t simple-api:latest .
   ```

2. **Load the new image into Minikube:**
   ```bash
   minikube image load simple-api:latest
   ```

3. **Trigger rolling update:**
   
   **Option A: Restart deployment (recommended for :latest tag):**
   ```bash
   kubectl rollout restart deployment simple-api
   ```
   
   **Option B: Set image directly:**
   ```bash
   kubectl set image deployment/simple-api simple-api=simple-api:latest
   ```
   
   **Option C: Update deployment manifest:**
   ```bash
   kubectl apply -f k8s/deployment.yaml
   ```

4. **Watch the rolling update:**
   ```bash
   # Watch rollout status
   kubectl rollout status deployment simple-api
   
   # Or watch pods being replaced in real-time
   kubectl get pods -l app=simple-api -w
   ```

5. **Verify the update:**
   ```bash
   # Check deployment history
   kubectl rollout history deployment simple-api
   
   # Check current pods
   kubectl get pods -l app=simple-api
   
   # View logs from new pods
   kubectl logs -l app=simple-api --tail=50
   ```

6. **Rollback if needed:**
   ```bash
   # Rollback to previous version
   kubectl rollout undo deployment simple-api
   
   # Or rollback to specific revision
   kubectl rollout undo deployment simple-api --to-revision=2
   ```

### Cleanup

To remove Kubernetes resources:
```bash
# Delete all resources in k8s directory
kubectl delete -f k8s/

# Or delete specific resources
kubectl delete deployment simple-api
kubectl delete service simple-api  # if service exists

# Stop Minikube (optional)
minikube stop
```

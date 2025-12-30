# Flask Task API

A simple Flask REST API for managing tasks, designed to demonstrate CI/CD with Jenkins.

## Features

- RESTful API endpoints for task management
- Web GUI with modern, responsive design
- Create, read, update, and delete tasks
- Health check endpoint
- Comprehensive unit tests
- Docker containerization
- Jenkins CI/CD pipeline integration

## API Endpoints

- `GET /` - Web GUI home page
- `GET /api` - API documentation
- `GET /health` - Health check endpoint
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/<id>` - Get a specific task
- `PUT /api/tasks/<id>` - Update a task
- `DELETE /api/tasks/<id>` - Delete a task

## Web Routes

- `POST /web/add` - Add task via web form
- `GET /web/toggle/<id>` - Toggle task completion
- `GET /web/delete/<id>` - Delete task via web

## Setup

### Prerequisites

- Python 3.8 or higher
- Docker (for containerized deployment)
- Jenkins (for CI/CD pipeline)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/deviant101/FlaskApp.git
   cd FlaskApp
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Local Development

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Using Docker

Build and run with Docker:
```bash
docker build -t flask-task-app .
docker run -d -p 5000:5000 --name flask-app-container flask-task-app
```

Or use Docker Compose:
```bash
docker-compose up -d
```

Stop the container:
```bash
docker-compose down
```

## Running Tests

Run all tests:
```bash
python -m pytest test_app.py -v
```

Run tests with coverage:
```bash
python -m pytest test_app.py --cov=app --cov-report=html
```

Run tests using unittest:
```bash
python -m unittest test_app.py
```

## Jenkins CI/CD Pipeline

This application includes a complete Jenkins pipeline (`Jenkinsfile`) that automates:

### Pipeline Stages

1. **Checkout** - Clone the repository
2. **Setup Python Environment** - Create virtual environment and install dependencies
3. **Run Tests** - Execute unit tests with coverage reporting
4. **Build Docker Image** - Build Docker image with build number tag
5. **Stop Old Container** - Remove existing container if running
6. **Deploy Container** - Start new container with the built image
7. **Health Check** - Verify application is running correctly
8. **Cleanup** - Remove old Docker images to save space

### Jenkins Setup

1. **Install Required Jenkins Plugins:**
   - Docker Pipeline
   - HTML Publisher
   - JUnit

2. **Create a new Pipeline job in Jenkins:**
   - Go to Jenkins → New Item → Pipeline
   - Configure SCM to point to your Git repository
   - Set Script Path to `Jenkinsfile`

3. **Configure Jenkins Environment:**
   - Ensure Docker is installed on Jenkins server
   - Add Jenkins user to docker group:
     ```bash
     sudo usermod -aG docker jenkins
     sudo systemctl restart jenkins
     ```

4. **Build the Pipeline:**
   - Click "Build Now"
   - Monitor the pipeline execution
   - View test results and coverage reports

### Pipeline Environment Variables

You can customize these in the Jenkinsfile:
- `DOCKER_IMAGE` - Docker image name (default: flask-task-app)
- `CONTAINER_NAME` - Container name (default: flask-app-container)
- `APP_PORT` - Application port (default: 5000)

### Pipeline Reports

After each build, Jenkins generates:
- **Test Results** - JUnit XML format
- **Coverage Report** - HTML coverage report
- **Build Artifacts** - Docker image with build tag

## Example Usage

### Create a task:
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task", "description": "Task description"}'
```

### Get all tasks:
```bash
curl http://localhost:5000/api/tasks
```

### Update a task:
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### Delete a task:
```bash
curl -X DELETE http://localhost:5000/api/tasks/1
```

### Health check:
```bash
curl http://localhost:5000/health
```

## Project Structure

```
.
├── app.py                 # Main Flask application
├── test_app.py           # Unit tests
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
├── Jenkinsfile           # Jenkins pipeline definition
├── .dockerignore         # Docker build exclusions
├── .gitignore           # Git exclusions
├── templates/
│   └── index.html       # Web GUI template
├── static/
│   └── style.css        # CSS styling
└── README.md            # This file
```

## Docker Image Details

- **Base Image:** python:3.13-slim
- **Exposed Port:** 5000
- **Health Check:** Built-in health check via `/health` endpoint
- **User:** Runs as non-root user (appuser)

## Troubleshooting

### Container won't start
```bash
docker logs flask-app-container
```

### Jenkins build fails
- Check Jenkins console output
- Verify Docker is accessible from Jenkins
- Ensure all required plugins are installed

### Port already in use
```bash
# Stop the existing container
docker stop flask-app-container
docker rm flask-app-container

# Or change the port in docker-compose.yml
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure they pass
5. Submit a pull request

## License

MIT License


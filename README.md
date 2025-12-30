# Flask Task API

A simple Flask REST API for managing tasks, designed to demonstrate CI/CD with Jenkins.

## Features

- RESTful API endpoints for task management
- Create, read, update, and delete tasks
- Health check endpoint
- Comprehensive unit tests
- Ready for Jenkins pipeline integration

## API Endpoints

- `GET /` - Home route with API documentation
- `GET /health` - Health check endpoint
- `GET /tasks` - Get all tasks
- `POST /tasks` - Create a new task
- `GET /tasks/<id>` - Get a specific task
- `PUT /tasks/<id>` - Update a task
- `DELETE /tasks/<id>` - Delete a task

## Setup

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository
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

```bash
python app.py
```

The application will start on `http://localhost:5000`

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

## Example Usage

### Create a task:
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task", "description": "Task description"}'
```

### Get all tasks:
```bash
curl http://localhost:5000/tasks
```

### Update a task:
```bash
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### Delete a task:
```bash
curl -X DELETE http://localhost:5000/tasks/1
```

## Jenkins Pipeline

This application is designed to work with Jenkins CI/CD. The pipeline will:
- Install dependencies
- Run tests
- Generate test reports
- Build and deploy the application

## Project Structure

```
.
├── app.py              # Main Flask application
├── test_app.py         # Unit tests
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

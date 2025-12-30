pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'flask-task-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = 'flask-app-container'
        APP_PORT = '5000'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    . venv/bin/activate
                    python -m pytest test_app.py -v --junitxml=test-results.xml --cov=app --cov-report=xml --cov-report=html
                '''
            }
            post {
                always {
                    // Publish test results
                    junit 'test-results.xml'
                    
                    // Publish coverage report
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                '''
            }
        }
        
        stage('Stop Old Container') {
            steps {
                echo 'Stopping and removing old container if exists...'
                sh '''
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                '''
            }
        }
        
        stage('Deploy Container') {
            steps {
                echo 'Starting new container...'
                sh '''
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${APP_PORT}:5000 \
                        --restart unless-stopped \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
            }
        }
        
        stage('Health Check') {
            steps {
                echo 'Performing health check...'
                sh '''
                    sleep 5
                    curl -f http://localhost:${APP_PORT}/health || exit 1
                '''
            }
        }
        
        stage('Cleanup') {
            steps {
                echo 'Cleaning up old Docker images...'
                sh '''
                    docker image prune -f
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
            echo "Application is running at http://localhost:${APP_PORT}"
        }
        failure {
            echo 'Pipeline failed!'
            sh 'docker logs ${CONTAINER_NAME} || true'
        }
        always {
            echo 'Cleaning up workspace...'
            cleanWs(deleteDirs: true, patterns: [[pattern: 'venv/**', type: 'INCLUDE']])
        }
    }
}

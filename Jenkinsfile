pipeline {
    agent any
    environment {
        IMAGE_NAME = 'smart-waste-management'
        CONTAINER_NAME = 'smart-waste-management-app'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Install dependencies and test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt pytest
                    pytest -q
                '''
            }
        }
        stage('Build Docker image') {
            steps { sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .' }
        }
        stage('Deploy locally') {
            steps {
                sh '''
                    docker rm -f ${CONTAINER_NAME} || true
                    docker volume create waste-data || true
                    docker run -d --name ${CONTAINER_NAME} --restart unless-stopped -p 5000:5000 -v waste-data:/data ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }
        stage('Smoke test') {
            steps {
                sh '''
                    for i in $(seq 1 15); do
                      if curl --fail http://localhost:5000/health; then exit 0; fi
                      sleep 2
                    done
                    echo "Application health check failed"
                    exit 1
                '''
            }
        }
    }
    post { always { echo 'Pipeline finished. Review stage logs for details.' } }
}

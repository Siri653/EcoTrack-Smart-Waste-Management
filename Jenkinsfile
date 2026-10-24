
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        IMAGE_NAME = 'ecotrack'
        CONTAINER_NAME = 'ecotrack-ci-cd-app'
        HOST_PORT = '5002'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies and test') {
            steps {
                withEnv(['SECRET_KEY=ecotrack-ci-test-only']) {
                    bat '''
                        if not exist ".venv\\Scripts\\python.exe" (
                            python -m venv .venv
                            if errorlevel 1 exit /b 1
                        )

                        ".venv\\Scripts\\python.exe" -m pip install --upgrade pip
                        if errorlevel 1 exit /b 1

                        ".venv\\Scripts\\python.exe" -m pip install -r requirements.txt pytest
                        if errorlevel 1 exit /b 1

                        ".venv\\Scripts\\python.exe" -m pytest -q
                    '''
                }
            }
        }

        stage('Build Docker image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
            }
        }

        
stage('Deploy locally') {
    steps {
        withCredentials([
            file(
                credentialsId: 'firebase-service-account',
                variable: 'FIREBASE_KEY_FILE'
            ),
            string(
                credentialsId: 'ecotrack-secret-key',
                variable: 'SECRET_KEY'
            )
        ]) {
            bat '''
                docker rm -f %CONTAINER_NAME% >NUL 2>&1

                if not exist "%FIREBASE_KEY_FILE%" (
                    echo Firebase credential file not found.
                    exit /b 1
                )

                set "FIREBASE_KEY_FILE_DOCKER=%FIREBASE_KEY_FILE:\\=/%"

                docker run -d --name %CONTAINER_NAME% --restart unless-stopped -p %HOST_PORT%:5000 -e "SECRET_KEY=%SECRET_KEY%" -e "GOOGLE_APPLICATION_CREDENTIALS=/run/secrets/firebase-service-account.json" --mount "type=bind,source=%FIREBASE_KEY_FILE_DOCKER%,target=/run/secrets/firebase-service-account.json,readonly" %IMAGE_NAME%:%BUILD_NUMBER%

                if errorlevel 1 exit /b 1
            '''
        }
    }
}


        stage('Smoke test') {
            steps {
                bat '''
                    for /L %%i in (1,1,15) do (
                        curl.exe --fail --silent http://localhost:%HOST_PORT%/health
                        if not errorlevel 1 exit /b 0
                        timeout /t 2 /nobreak >NUL
                    )

                    echo Application health check failed
                    exit /b 1
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished. Review stage logs for details.'
        }
    }
}

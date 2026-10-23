# EcoTrack — Smart Waste Management System

A Flask + SQLite web app for a DevOps case study. Users can submit waste reports; the demo admin interface can update their status.

## Features
- Submit waste reports with name, location, type, and description
- Dashboard counts for total, pending, in-progress, and completed reports
- Update report status
- SQLite persistence and `/health` endpoint
- Pytest tests, Dockerfile, and Jenkins pipeline

## Run locally on Windows
1. Install Python 3.11+ and open this folder in VS Code.
2. In the VS Code terminal, run:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python app.py
   ```

3. Open `http://127.0.0.1:5000`.

If PowerShell blocks activation, use `python -m pip install -r requirements.txt` and `python app.py` without activating the environment.

## Run tests
```powershell
python -m pip install pytest
python -m pytest -q
```

## Run with Docker
Make sure Docker Desktop is running. In the project folder:

```powershell
docker build -t smart-waste-management .
docker volume create waste-data
docker run -d --name smart-waste-management-app -p 5000:5000 -v waste-data:/data smart-waste-management
```

Open `http://localhost:5000`. To stop/remove the container: `docker rm -f smart-waste-management-app`.

## DevOps pipeline
1. Develop and test locally.
2. Push all files to GitHub.
3. Configure a Jenkins Pipeline job to use the repository and `Jenkinsfile`.
4. Use a Linux Jenkins agent with Python 3, pip, Docker CLI/daemon access, and curl.
5. Run the pipeline: checkout → tests → Docker build → local container deployment → health check.

The Jenkinsfile uses Unix `sh` commands and is intended for a Linux Jenkins agent with Docker access. It deploys to the Jenkins agent machine, so treat it as a learning/demo pipeline. Configure Docker access securely and do not expose the Docker daemon publicly. The status update feature is a demo admin interface without authentication; add authentication and authorization before using real data.

## Structure
```text
smart_waste_management/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── Jenkinsfile
├── README.md
├── templates/index.html
├── static/style.css
└── tests/test_app.py
```

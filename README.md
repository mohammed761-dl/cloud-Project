# 🚀 Cloud-Native User Management Application

A containerized microservices application featuring a FastAPI backend and responsive frontend, orchestrated with Kubernetes and automated through Jenkins CI/CD pipeline.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [DevOps Pipeline](#devops-pipeline)
- [Azure Integration](#azure-integration)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Project Structure](#project-structure)

---

## 🎯 Overview

This project demonstrates a complete DevOps workflow for deploying a cloud-native application with:

- **Backend**: FastAPI-based RESTful API for user management
- **Frontend**: Nginx-served static web interface
- **Containerization**: Docker for consistent deployment
- **Orchestration**: Kubernetes for container management
- **CI/CD**: Jenkins pipeline with automated build, push, and deployment
- **Configuration Management**: Ansible for infrastructure automation

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    JENKINS CI/CD                        │
│  ┌──────────┐  ┌──────────┐  ┌─────────┐  ┌─────────┐ │
│  │  Build   │→ │   Push   │→ │ Ansible │→ │ Deploy  │ │
│  │  Docker  │  │ Registry │  │  K8s    │  │ Rollout │ │
│  └──────────┘  └──────────┘  └─────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│              KUBERNETES CLUSTER (K3s)                   │
│  ┌──────────────────┐      ┌──────────────────┐        │
│  │  Frontend Pod    │      │   Backend Pod    │        │
│  │  (Nginx)         │  →   │   (FastAPI)      │        │
│  │  NodePort: 30081 │      │   NodePort: 30080│        │
│  └──────────────────┘      └──────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Application Layer

- **Backend**: FastAPI (Python 3.10)
- **Frontend**: HTML/CSS/JavaScript with Nginx
- **Database**: In-memory storage (ready for Azure SQL/PostgreSQL)

### DevOps & Infrastructure

- **CI/CD**: Jenkins Pipeline
- **Containerization**: Docker
- **Orchestration**: Kubernetes (K3s)
- **Configuration Management**: Ansible
- **Container Registry**: Docker Registry (Gitea-hosted)

### Cloud Platform (Azure Ready)

- **Azure Kubernetes Service (AKS)**: For managed Kubernetes
- **Azure Container Registry (ACR)**: For private Docker images
- **Azure DevOps Pipelines**: Alternative to Jenkins
- **Azure SQL Database**: For persistent storage
- **Azure Key Vault**: For secrets management

---

## 🔄 DevOps Pipeline

### Pipeline Stages

#### 1️⃣ **Build & Push Backend**

```groovy
- Builds Docker image from backend/Dockerfile
- Tags with build number and 'latest'
- Authenticates to Docker registry
- Pushes images to registry
```

#### 2️⃣ **Build & Push Frontend**

```groovy
- Builds Docker image from frontend/Dockerfile
- Tags with build number and 'latest'
- Authenticates to Docker registry
- Pushes images to registry
```

#### 3️⃣ **Deploy with Ansible**

```yaml
- Applies Kubernetes manifests
- Deploys backend (user-management-app)
- Deploys frontend (frontend-app)
- Uses K3s configuration
```

#### 4️⃣ **Force Refresh for Demo**

```bash
- Triggers rolling restart of deployments
- Ensures latest images are pulled
- Waits for rollout completion
```

### Pipeline Environment Variables

| Variable          | Description                 |
| ----------------- | --------------------------- |
| `DOCKER_REGISTRY` | Docker registry URL         |
| `BACKEND_IMAGE`   | Backend image name          |
| `FRONTEND_IMAGE`  | Frontend image name         |
| `TAG`             | Build number for versioning |

### Credentials Required

- `gitea-docker-credentials`: Docker registry authentication
- `k3s-config`: Kubernetes cluster configuration

---

## ☁️ Azure Integration

### Option 1: Azure Kubernetes Service (AKS)

#### Setup AKS Cluster

```bash
# Create resource group
az group create --name cloud-project-rg --location eastus

# Create AKS cluster
az aks create \
  --resource-group cloud-project-rg \
  --name cloud-project-aks \
  --node-count 2 \
  --enable-managed-identity \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group cloud-project-rg --name cloud-project-aks
```

#### Update Jenkinsfile for AKS

```groovy
environment {
    ACR_REGISTRY = 'yourregistry.azurecr.io'
    AKS_CLUSTER = 'cloud-project-aks'
    RESOURCE_GROUP = 'cloud-project-rg'
}

stage('Deploy to AKS') {
    steps {
        sh """
            az aks get-credentials --resource-group ${RESOURCE_GROUP} --name ${AKS_CLUSTER}
            kubectl apply -f backend/k8s-deploy.yaml
            kubectl apply -f frontend/k8s-frontend-deploy.yaml
        """
    }
}
```

### Option 2: Azure Container Registry (ACR)

```bash
# Create ACR
az acr create \
  --resource-group cloud-project-rg \
  --name cloudprojectacr \
  --sku Basic

# Login to ACR
az acr login --name cloudprojectacr

# Update Jenkinsfile
DOCKER_REGISTRY = 'cloudprojectacr.azurecr.io'
```

### Option 3: Azure DevOps Pipelines

Create `azure-pipelines.yml`:

```yaml
trigger:
  - main

pool:
  vmImage: "ubuntu-latest"

variables:
  acrName: "cloudprojectacr"
  aksCluster: "cloud-project-aks"
  resourceGroup: "cloud-project-rg"

stages:
  - stage: Build
    jobs:
      - job: BuildAndPush
        steps:
          - task: Docker@2
            inputs:
              containerRegistry: "ACR-Connection"
              repository: "backend"
              command: "buildAndPush"
              Dockerfile: "backend/Dockerfile"
              tags: |
                $(Build.BuildId)
                latest

  - stage: Deploy
    jobs:
      - job: DeployToAKS
        steps:
          - task: KubernetesManifest@0
            inputs:
              action: "deploy"
              kubernetesServiceConnection: "AKS-Connection"
              manifests: |
                backend/k8s-deploy.yaml
                frontend/k8s-frontend-deploy.yaml
```

### Azure SQL Integration

Update `backend/main.py` for Azure SQL:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Azure SQL Connection String
DATABASE_URL = os.getenv(
    "AZURE_SQL_CONNECTION_STRING",
    "mssql+pyodbc://username:password@server.database.windows.net/dbname?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

---

## 🚀 Getting Started

### Prerequisites

- Docker installed
- Kubernetes cluster (K3s/AKS)
- Jenkins server
- Ansible installed
- kubectl configured

### Local Development

#### 1. Clone the repository

```bash
git clone <repository-url>
cd cloud-Project
```

#### 2. Run Backend Locally

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### 3. Access API Documentation

```
http://localhost:8000/docs
```

#### 4. Run Frontend Locally

```bash
cd frontend
python -m http.server 8080
```

---

## 📦 Deployment

### Manual Deployment

#### 1. Build Docker Images

```bash
# Backend
docker build -t user-mgmt-api:latest ./backend

# Frontend
docker build -t frontend:latest ./frontend
```

#### 2. Push to Registry

```bash
docker tag user-mgmt-api:latest your-registry/user-mgmt-api:latest
docker push your-registry/user-mgmt-api:latest

docker tag frontend:latest your-registry/frontend:latest
docker push your-registry/frontend:latest
```

#### 3. Deploy to Kubernetes

```bash
kubectl apply -f backend/k8s-deploy.yaml
kubectl apply -f frontend/k8s-frontend-deploy.yaml
```

#### 4. Verify Deployment

```bash
kubectl get pods
kubectl get services
```

### Automated Deployment (Jenkins)

1. Push code to Git repository
2. Jenkins detects changes (webhook/polling)
3. Pipeline automatically:
   - Builds Docker images
   - Pushes to registry
   - Deploys to Kubernetes
   - Performs rolling updates

---

## 📁 Project Structure

```
cloud-Project/
├── backend/
│   ├── Dockerfile              # Backend container definition
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   └── k8s-deploy.yaml         # Kubernetes deployment manifest
├── frontend/
│   ├── Dockerfile              # Frontend container definition
│   ├── index.html              # Web interface
│   └── k8s-frontend-deploy.yaml # Kubernetes deployment manifest
├── ansible/
│   └── deploy.yml              # Ansible playbook for deployment
├── Jenkinsfile                 # CI/CD pipeline definition
└── README.md                   # This file
```

---

## 🔧 Configuration

### Backend Configuration

- **Port**: 8000
- **Replicas**: 2
- **Service Type**: NodePort (30080)
- **Image Pull Policy**: Always

### Frontend Configuration

- **Port**: 80
- **Replicas**: 1
- **Service Type**: NodePort (30081)
- **Image Pull Policy**: Always

---

## 🔐 Security Best Practices

### For Azure Deployment:

1. **Use Azure Key Vault** for secrets management
2. **Enable Azure AD Integration** for AKS
3. **Implement Network Policies** in Kubernetes
4. **Use Azure Private Link** for database connections
5. **Enable Azure Security Center** for threat detection
6. **Use Managed Identities** instead of service principals

---

## 📊 Monitoring & Logging

### Current Setup

- Jenkins build logs
- Kubernetes pod logs: `kubectl logs <pod-name>`

### Azure Monitoring

```bash
# Enable Azure Monitor for AKS
az aks enable-addons \
  --resource-group cloud-project-rg \
  --name cloud-project-aks \
  --addons monitoring
```

### Application Insights Integration

Add to `backend/main.py`:

```python
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=<your-key>'
))
```

---

## 🧪 API Endpoints

| Method | Endpoint      | Description         |
| ------ | ------------- | ------------------- |
| GET    | `/`           | API status and info |
| POST   | `/users/`     | Create new user     |
| GET    | `/users/`     | List all users      |
| GET    | `/users/{id}` | Get user by ID      |
| DELETE | `/users/{id}` | Delete user         |

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👥 Authors

- **Mohammed Cherkaoui** - Owner & Initial work

---

## 🙏 Acknowledgments

- FastAPI for excellent Python web framework
- Kubernetes for container orchestration
- Jenkins for CI/CD automation
- Azure for cloud infrastructure

---

## 📞 Support

For issues and questions:

- Create an issue in the repository
- Contact: [Your Email]

---

**Made with ❤️ for DevOps Excellence**

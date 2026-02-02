
# Grafana on ECS/Fargate with Terraform

This project automates the deployment of a custom Grafana service on AWS ECS Fargate using Terraform. It supports credential-free access to CloudWatch data sources, includes CI/CD, custom Docker image build, and follows least-privilege IAM best practices.

## Features
- One-click deployment of custom Grafana to AWS ECS Fargate
- Automatic IAM role configuration for credential-free Grafana access to CloudWatch Logs
- Dockerfile supports custom plugins and pre-provisioned dashboards/datasources
- Makefile for image build and push
- Modular Terraform code structure, easy to extend

## Quick Start

### 1. Prerequisites
- Docker & Docker Compose
- Terraform >= 1.3
- AWS CLI with valid credentials

### 2. Build and Push Docker Image
```sh
# Build local image
make local-build
# Push image to Docker Hub
make push
```

### 3. Deploy to AWS
```sh
cd terraform_dns_automation
terraform init
terraform apply
```

### 4. Local Development & Debugging
```sh
# Start local Grafana
make up
# View logs
make logs
# Stop and clean up
make down
make clean
```

## Directory Structure
terraform_dns_automation/   # Main Terraform directory
Dockerfile.grafana         # Grafana image build file
Makefile                   # Common build/ops commands
bitbucket-pipelines.yml    # CI/CD configuration
docker-compose.yml         # Local multi-container config

## Common Commands
- make build        Build Grafana image
- make push         Push image to registry
- make up/down      Start/stop local container
- make logs         View Grafana logs
- make lint         Dockerfile syntax check

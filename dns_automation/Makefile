# Makefile for managing Grafana Docker container and image

up:
	docker compose up -d

down:
	docker compose down -v

logs:
	docker compose logs -f grafana

clean:
	docker compose down -v && rm -rf grafana-data

restart:
	docker compose restart grafana

# Image name and tag for Grafana
GRAFANA_IMAGE ?= jessamy/grafana-custom
TAG ?= v1.0.0

lint:
	docker run --rm -v $(PWD):/app hadolint/hadolint hadolint /app/terraform_dns_automation/Dockerfile.grafana

# Build Grafana Docker image
build:
	docker build --platform linux/amd64 -t $(GRAFANA_IMAGE):$(TAG) -f terraform_dns_automation/Dockerfile.grafana .

# Local build for development (with buildx)
local-build:
	docker buildx build --platform linux/amd64 -t $(GRAFANA_IMAGE):$(TAG) -f terraform_dns_automation/Dockerfile.grafana . --load

# Push Grafana image to Docker Hub
push:
	docker push $(GRAFANA_IMAGE):$(TAG)


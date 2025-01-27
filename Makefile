# Variables
VERSION ?= 3.0.2
DOCKER_USER=andrewjsc
BACKEND_IMAGE=$(DOCKER_USER)/bmsisp-backend
FRONTEND_IMAGE=$(DOCKER_USER)/bmsisp-frontend
BACKEND_DIR=./backend
FRONTEND_DIR=./frontend

# Targets
.PHONY: backend frontend build push dev prod detect-platform

# Detect Architecture and Set TARGET_PLATFORM
detect-platform:
	@ARCH=$$(uname -m); \
	if [ "$$ARCH" = "x86_64" ]; then \
	  echo "Detected architecture: $$ARCH (amd64)"; \
	  TARGET_PLATFORM="linux/amd64"; \
	elif [ "$$ARCH" = "arm64" ]; then \
	  echo "Detected architecture: $$ARCH (arm64)"; \
	  TARGET_PLATFORM="linux/arm64"; \
	else \
	  echo "Unsupported architecture: $$ARCH"; \
	  exit 1; \
	fi; \
	export TARGET_PLATFORM=$$TARGET_PLATFORM; \
	echo "Using TARGET_PLATFORM=$$TARGET_PLATFORM"

# Native build for current architecture
build: detect-platform
	@echo "Building natively"; \
	$(MAKE) backend frontend

backend:
	docker build -t $(BACKEND_IMAGE):$(VERSION)-alpha -f $(BACKEND_DIR)/Dockerfile ${BACKEND_DIR}

frontend:
	docker build -t $(FRONTEND_IMAGE):$(VERSION)-alpha -f $(FRONTEND_DIR)/Dockerfile ${FRONTEND_DIR}

prod:
	@echo "Building for Windows (targeting linux/amd64)"; \
	$(MAKE) backend-prod frontend-prod

backend-prod:
	docker buildx build --platform linux/amd64 -t $(BACKEND_IMAGE):$(VERSION) --push $(BACKEND_DIR)

frontend-prod:
	docker buildx build --platform linux/amd64 -t $(FRONTEND_IMAGE):$(VERSION) --push $(FRONTEND_DIR)

push:
	@echo "Building for Windows (targeting linux/amd64)"; \
	docker buildx build --platform linux/amd64 -t $(BACKEND_IMAGE):$(VERSION)-alpha --push $(BACKEND_DIR)
	docker buildx build --platform linux/amd64 -t $(FRONTEND_IMAGE):$(VERSION)-alpha --push $(FRONTEND_DIR)

# Run Docker Compose with dynamic architecture detection
dev: detect-platform
	@ARCH=$$(uname -m); \
	if [ "$$ARCH" = "x86_64" ]; then \
	  TARGET_PLATFORM="linux/amd64"; \
	elif [ "$$ARCH" = "arm64" ]; then \
	  TARGET_PLATFORM="linux/arm64"; \
	else \
	  echo "Unsupported architecture: $$ARCH"; \
	  exit 1; \
	fi; \
	echo "Starting Docker Compose with TARGET_PLATFORM=$$TARGET_PLATFORM"; \
	VERSION=$(VERSION)-alpha TARGET_PLATFORM=$$TARGET_PLATFORM docker-compose up -d

kill:
	docker-compose down

# Variables
VERSION ?= 3.0.1-alpha
DOCKER_USER=andrewjsc
BACKEND_IMAGE=$(DOCKER_USER)/bmsisp-backend:$(VERSION)
FRONTEND_IMAGE=$(DOCKER_USER)/bmsisp-frontend:$(VERSION)
BACKEND_DIR=./backend
FRONTEND_DIR=./frontend

# Targets
.PHONY: backend frontend backend-prod frontend-prod all prod dev detect-platform

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
all: detect-platform
	@echo "Building natively"; \
	$(MAKE) backend frontend

backend:
	docker build -t $(BACKEND_IMAGE) $(BACKEND_DIR)

frontend:
	docker build -t $(FRONTEND_IMAGE) $(FRONTEND_DIR)

prod:
	@echo "Building for Windows (targeting linux/amd64)"; \
	$(MAKE) backend-prod frontend-prod

backend-prod:
	docker buildx build --platform linux/amd64 -t $(BACKEND_IMAGE) --push $(BACKEND_DIR)

frontend-prod:
	docker buildx build --platform linux/amd64 -t $(FRONTEND_IMAGE) --push $(FRONTEND_DIR)

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
	VERSION=$(VERSION) TARGET_PLATFORM=$$TARGET_PLATFORM docker-compose up -d

kill:
	docker-compose down

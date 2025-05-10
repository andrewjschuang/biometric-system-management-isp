# Variables
VERSION ?= 3.0.4
DOCKER_USER = andrewjsc
BACKEND_IMAGE = $(DOCKER_USER)/bmsisp-backend
FRONTEND_IMAGE = $(DOCKER_USER)/bmsisp-frontend
PRESENCE_IMAGE = $(DOCKER_USER)/bmsisp-presence
BACKEND_DIR = ./backend
FRONTEND_DIR = ./frontend
PRESENCE_DIR = ./presence

# Phony targets
.PHONY: all build prod presence frontend backend presence-prod frontend-prod backend-prod detect-platform dev kill

# Detect architecture and set TARGET_PLATFORM
detect-platform:
	@ARCH=$$(uname -m); \
	if [ "$$ARCH" = "x86_64" ]; then \
	  export TARGET_PLATFORM="linux/amd64"; \
	elif [ "$$ARCH" = "arm64" ]; then \
	  export TARGET_PLATFORM="linux/arm64"; \
	else \
	  echo "Unsupported architecture: $$ARCH"; exit 1; \
	fi; \
	echo "Using TARGET_PLATFORM=$$TARGET_PLATFORM";

# Default target
all: build

# Build all services locally for current architecture
build: detect-platform presence frontend backend
	@echo "✅ All services built locally."

# Individual local-build targets\presence:
	docker build -t $(PRESENCE_IMAGE):$(VERSION)-alpha \
	  --platform=$$TARGET_PLATFORM -f $(PRESENCE_DIR)/Dockerfile $(PRESENCE_DIR)

backend:
	docker build -t $(BACKEND_IMAGE):$(VERSION)-alpha \
	  --platform=$$TARGET_PLATFORM -f $(BACKEND_DIR)/Dockerfile $(BACKEND_DIR)

frontend:
	docker build -t $(FRONTEND_IMAGE):$(VERSION)-alpha \
	  --platform=$$TARGET_PLATFORM -f $(FRONTEND_DIR)/Dockerfile $(FRONTEND_DIR)

presence:
	docker build -t $(PRESENCE_IMAGE):$(VERSION)-alpha \
	  --platform=$$TARGET_PLATFORM -f $(PRESENCE_DIR)/Dockerfile $(PRESENCE_DIR)

# Build and push all services for production (amd64)
prod: presence-prod frontend-prod backend-prod
	@echo "🚀 All production images built and pushed."

# Individual prod targets
presence-prod:
	docker buildx build --platform linux/amd64 \
	  -t $(PRESENCE_IMAGE):$(VERSION) --push $(PRESENCE_DIR)

backend-prod:
	docker buildx build --platform linux/amd64 \
	  -t $(BACKEND_IMAGE):$(VERSION) --push $(BACKEND_DIR)

frontend-prod:
	docker buildx build --platform linux/amd64 \
	  -t $(FRONTEND_IMAGE):$(VERSION) --push $(FRONTEND_DIR)

# Start docker-compose using dynamic architecture detection
dev: detect-platform
	@ARCH=$$(uname -m); \
	if [ "$$ARCH" = "x86_64" ]; then \
	  export TARGET_PLATFORM="linux/amd64"; \
	elif [ "$$ARCH" = "arm64" ]; then \
	  export TARGET_PLATFORM="linux/arm64"; \
	else \
	  echo "Unsupported architecture: $$ARCH"; exit 1; \
	fi; \
	echo "Starting Docker Compose with TARGET_PLATFORM=$$TARGET_PLATFORM"; \
	VERSION=$(VERSION)-alpha TARGET_PLATFORM=$$TARGET_PLATFORM docker-compose up -d

# Stop docker-compose
kill:
	docker-compose down

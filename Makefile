# Variables
MAKEFLAGS += -j3
VERSION ?= 3.0.9
DOCKER_USER = andrewjsc
BACKEND_IMAGE = $(DOCKER_USER)/bmsisp-backend
FRONTEND_IMAGE = $(DOCKER_USER)/bmsisp-frontend
PRESENCE_IMAGE = $(DOCKER_USER)/bmsisp-presence
BACKEND_DIR = ./backend
FRONTEND_DIR = ./frontend
PRESENCE_DIR = ./presence

# Phony targets
.PHONY: build prod presence frontend backend presence-prod frontend-prod backend-prod detect-platform dev kill up

up: detect-platform
	@echo "Starting containers..."
	VERSION=$(VERSION)-alpha TARGET_PLATFORM=$$TARGET_PLATFORM docker-compose up -d

# Start docker-compose using dynamic architecture detection
dev: build
	VERSION=$(VERSION)-alpha TARGET_PLATFORM=$$TARGET_PLATFORM docker-compose up -d

# Stop docker-compose
kill:
	docker-compose down

# Build all services locally for current architecture
build: presence frontend backend
	@echo "✅ All services built locally."

# Build and push all services for production (amd64)
prod: presence-prod frontend-prod backend-prod
	@echo "🚀 All production images built and pushed."

# Individual local-build targets\presence:
backend: detect-platform
	docker build -t $(BACKEND_IMAGE):$(VERSION)-alpha \
	  --platform=$$TARGET_PLATFORM -f $(BACKEND_DIR)/Dockerfile $(BACKEND_DIR)

frontend: detect-platform
	docker build -t $(FRONTEND_IMAGE):$(VERSION)-alpha \
	  --platform=$$TARGET_PLATFORM -f $(FRONTEND_DIR)/Dockerfile $(FRONTEND_DIR)

presence: detect-platform
	docker build -t $(PRESENCE_IMAGE):$(VERSION)-alpha \
	  --platform=$$TARGET_PLATFORM -f $(PRESENCE_DIR)/Dockerfile $(PRESENCE_DIR)

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

TAG=andrewjsc/bmsisp-backend:3.0.0-alpha

# Create and use a new builder instance
docker buildx create --name backendbuilder --use

# Inspect to see the current configuration
docker buildx inspect --bootstrap

# Build the multi-architecture image
docker buildx build --platform linux/amd64,linux/arm64 -t $TAG --push .

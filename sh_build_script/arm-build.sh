#!/bin/bash

set -e

# Default platform to amd64
ARCH=${1:-arm64}
VERSION="v1.0.0"

# Map to Docker platform
if [ "$ARCH" == "amd64" ]; then
    PLATFORM="linux/amd64"
elif [ "$ARCH" == "arm64" ]; then
    PLATFORM="linux/arm64"
else
    echo "Unsupported architecture: $ARCH"
    echo "Usage: ./build-base-image.sh [amd64|arm64]"
    exit 1
fi

# Ensure buildx is available
if ! docker buildx version > /dev/null 2>&1; then
    echo "Docker Buildx is not installed or not configured. Please install it first."
    exit 1
fi

# Use a named builder or create one if not exist
BUILDER_NAME="amd_builder"
if ! docker buildx inspect "$BUILDER_NAME" >/dev/null 2>&1; then
    docker buildx create --name "$BUILDER_NAME" --use
else
    docker buildx use "$BUILDER_NAME"
fi

# Build the image
docker buildx build \
    --platform "$PLATFORM" \
    -f DockerfileARM \
    -t dattran453/base-image:"$ARCH-$VERSION" \
    --push .  # `--push` pushes image to registry

echo "✅ Pushed image: dattran453/base-image:$ARCH-$VERSION"
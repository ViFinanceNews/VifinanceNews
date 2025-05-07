#!/bin/bash

set -e

# Default platform to amd64
ARCH=${1:-amd64}
VERSION="v1.0.0"

services=(
  "SearchService"
  "SummariserService"
  "AnalysisService"
  "LoggingService"
)


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



build_service() {
  service=$1
  name=$(echo "$service" | sed 's/Service$//' | tr '[:upper:]' '[:lower:]' | awk '{print $0 "_service"}')
  echo "🔨 Building $name for $ARCH..."

  dockerfile="$service/DockerfileAMD"
  if [ ! -f "$dockerfile" ]; then
    echo "❌ Dockerfile not found: $dockerfile"
    exit 1
  fi

  if docker buildx build \
    --platform "$PLATFORM" \
    -f $dockerfile \
    -t dattran453/"$name":"$VERSION-$ARCH" \
    --push .  # `--push` pushes image to registry
  then
    echo "✅ Pushed image: dattran453/base-image:$ARCH-$VERSION" # Build the image
  else
    echo "❌ Failed to build and push: $name"
    exit 1
  fi
}

# Export function for parallel execution
export -f build_service
export ARCH VERSION PLATFORM

printf "%s\n" "${services[@]}" | xargs -n 1 -P 4 -I {} bash -c 'build_service "$@"' _ {}

echo "🎉 All $ARCH images built and pushed successfully!"



#!/bin/bash

# Define the architecture to build for (default to amd64)
ARCH="${1:-amd64}"
PLATFORM="linux/$ARCH"
TYPE="AMD"

# Define the version
VERSION="v1.0.3"

# Define the services to be built and pushed
services=(
  "SearchService"
  "SummariserService"
  "AnalysisService"
  "LoggingService"
)

build_service() {
  service=$1
  name=$(echo "$service" | sed 's/Service$//' | tr '[:upper:]' '[:lower:]' | awk '{print $0 "_service"}')
  echo "🔨 Building $name for $ARCH..."

  if docker buildx build --platform "$PLATFORM" \
    -t dattran453/"$name":$VERSION-$ARCH \
    -f "$service"/Dockerfile$TYPE \
    --cache-to=type=registry,ref=dattran453/"$name"-$ARCH-cache:latest,mode=max \
    . \
    --push; then
    echo "✅ Built and pushed: $name ($ARCH)"
  else
    echo "❌ Failed to build and push: $name"
    exit 1
  fi
}

# Export function for parallel execution
export -f build_service

# Run builds in parallel
printf "%s\n" "${services[@]}" | xargs -n 1 -P 4 -I {} bash -c 'build_service "$@"' _ {}

echo "🎉 All $ARCH images built and pushed successfully!"
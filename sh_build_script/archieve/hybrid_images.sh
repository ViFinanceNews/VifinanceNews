#!/bin/bash

set -euo pipefail

export VERSION="v1.0.3"

# 📦 List of microservices to build and push
services=(
  "SearchService"
  "SummariserService"
  "AnalysisService"
  "LoggingService"
)

# 🏗️ Ensure a buildx builder exists and is active
if ! docker buildx inspect mybuilder &>/dev/null; then
  echo "🔧 Creating new buildx builder: mybuilder"
  docker buildx create --name mybuilder --driver docker-container --use
else
  echo "🔁 Reusing existing builder: mybuilder"
  docker buildx use mybuilder
fi

docker buildx inspect --bootstrap

# 🔨 Build function for each service
build_service() {
  local service="$1"
  local name
  name=$(echo "$service" | sed 's/Service$//' | tr '[:upper:]' '[:lower:]')_service

  echo "🚀 Building image: $name"

  if docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t "dattran453/${name}:${VERSION}" \
    -f "${service}/Dockerfile" \
    --cache-to=type=registry,ref="dattran453/${name}-cache:${VERSION}",mode=max \
    . \
    --push; then
    echo "✅ Successfully built and pushed: $name"
  else
    echo "❌ Build failed for: $name"
    exit 1
  fi
}

export -f build_service

# 🧵 Run builds in parallel
echo "📦 Starting parallel builds for services..."
printf "%s\n" "${services[@]}" | xargs -n 1 -P 4 -I {} bash -c 'build_service "$@"' _ {}

echo "🎉 All service images built and pushed successfully!"
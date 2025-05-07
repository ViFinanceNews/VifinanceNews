#!/bin/bash

set -euo pipefail

export VERSION="v1.0.3"
export PLATFORM="linux/amd64"  # or "linux/arm64" depending on your need

# 📦 List of microservices to build and store locally
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

  echo "🚀 Building image locally: $name for ${PLATFORM}"

  if docker buildx build \
    --platform "${PLATFORM}" \
    -t "dattran453/${name}:${VERSION}" \
    -f "${service}/Dockerfile" \
    --output type=docker \
    .; then
    echo "✅ Successfully built locally: $name"
  else
    echo "❌ Build failed for: $name"
    exit 1
  fi
}

export -f build_service

# 🧵 Run builds in parallel
echo "📦 Starting parallel local builds for services..."
printf "%s\n" "${services[@]}" | xargs -n 1 -P 4 -I {} bash -c 'build_service "$@"' _ {}

echo "🎉 All service images built and stored locally!"
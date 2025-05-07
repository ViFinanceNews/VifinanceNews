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

# 🏗️ Ensure a buildx builder with the correct driver exists and is active
ensure_builder() {
  local builder="mybuilder"
  local driver

  if docker buildx inspect "$builder" &>/dev/null; then
    driver=$(docker buildx inspect "$builder" | grep -i 'Driver:' | awk '{print $2}')
    if [[ "$driver" != "docker-container" ]]; then
      echo "⚠️  Existing builder '$builder' uses driver '$driver'. Recreating with 'docker-container'..."
      docker buildx rm "$builder"
      docker buildx create --name "$builder" --driver docker-container --use
    else
      echo "🔁 Reusing existing builder: $builder"
      docker buildx use "$builder"
    fi
  else
    echo "🔧 Creating new buildx builder: $builder"
    docker buildx create --name "$builder" --driver docker-container --use
  fi

  docker buildx inspect --bootstrap
}

ensure_builder

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

# 🧱 Run builds sequentially
echo "📦 Starting sequential builds for services..."
for service in "${services[@]}"; do
  build_service "$service"
done

echo "🎉 All service images built and pushed successfully!"
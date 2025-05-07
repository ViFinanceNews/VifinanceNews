#!/bin/bash

# Define the services to be built and pushed
services=(
  "SearchService"
  "SummariserService"
  "AnalysisService"
  "LoggingService"
)

for service in "${services[@]}"; do
  name=$(echo "$service" | sed 's/Service$//' | tr '[:upper:]' '[:lower:]' | awk '{print $0 "_service"}')

  echo "🔨 Building $name..."

  if docker buildx build --platform linux/amd64,linux/arm64 \
    -t dattran453/"$name":v1.0.3 \
    -f "$service"/Dockerfile-1.0.2 \
    --cache-to=type=registry,ref=dattran453/"$name"-cache:latest,mode=max \
    . \
    --push; then
    echo "✅ Built and pushed: $name"
  else
    echo "❌ Failed to build and push: $name"
    exit 1
  fi
done

echo "🎉 All images built and pushed sequentially!"
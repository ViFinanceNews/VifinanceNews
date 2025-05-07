#!/bin/sh

set -e

VERSION=1.0.1
ARCH=amd64
TYPE=AMD
PLATFORM=linux/amd64
IMAGE_NAME=dattran453/base-image

echo "🔨 Building base image for $ARCH..."

docker buildx build \
  --platform "$PLATFORM" \
  -f Dockerfile$TYPE \
  -t "$IMAGE_NAME":"$ARCH-v$VERSION" \
  --push .

echo "✅ Successfully pushed $IMAGE_NAME:$ARCH-v$VERSION"
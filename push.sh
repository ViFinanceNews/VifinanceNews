#!/bin/bash

VERSION="v1.0.2"
USERNAME="dattran453"

SERVICES=(
  logging_service
  analysis_service
  summariser_service
  search_service
  user_service
  authentication_service
)

for service in "${SERVICES[@]}"; do
  echo "Pushing $USERNAME/$service:$VERSION..."
  docker push "$USERNAME/$service:$VERSION"
done
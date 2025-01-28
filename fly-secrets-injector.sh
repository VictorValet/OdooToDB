#!/bin/bash

# Collect all key-value pairs
secrets=""

while IFS= read -r line; do
  # Skip empty lines and lines starting with #
  if [[ -n "$line" && "$line" != \#* ]]; then
    IFS='=' read -r name value <<< "$line"
    # Ensure name and value are not empty
    if [[ -n "$name" && -n "$value" ]]; then
      secrets="$secrets $name=$value"
    fi
  fi
done < .env

# Set all secrets at once
if [[ -n "$secrets" ]]; then
  flyctl secrets set $secrets
fi
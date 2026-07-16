#!/usr/bin/env bash
# Chapter 10 - Using code-generation tools (OpenAPI Generator).
# Generates a Python FastAPI server stub from the spec, so the contract drives the code.
set -euo pipefail

# Requires: npm i -g @openapitools/openapi-generator-cli  (or the jar)
openapi-generator-cli generate \
  -i petstore.yaml \
  -g python-fastapi \
  -o ./generated-server

echo "Generated server stub in ./generated-server"
echo "Swagger Codegen alternative:"
echo "  swagger-codegen generate -i petstore.yaml -l python-flask -o ./generated-flask"

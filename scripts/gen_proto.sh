#!/usr/bin/env bash
# Regenerate src/wispr_client/_proto/flow_api_v1_pb2.py from proto/flow_api_v1.proto.
# Requires grpcio-tools (uv pip install grpcio-tools). The protobuf runtime pin in
# pyproject.toml must stay >= the protobuf version bundled with grpcio-tools.
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${PYTHON:-.venv/bin/python}"
"$PY" -m grpc_tools.protoc -I proto --python_out=src/wispr_client/_proto --pyi_out=src/wispr_client/_proto proto/flow_api_v1.proto
"$PY" -c "import google.protobuf; print('generated with protobuf', google.protobuf.__version__)"

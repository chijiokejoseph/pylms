#!/bin/bash
# Build all Rust extension modules

echo "Activate Python Environment"
source .venv/Scripts/activate

set -e

echo "Sync UV environment"
uv sync

echo "Building Rust Modules"
cd pyrs

echo "Building rclean..."
cd rclean
maturin develop --release
cd ..

echo "Building rmpath..."
cd rmpath
maturin develop --release
cd ..

echo "All modules built successfully!"
cd ..

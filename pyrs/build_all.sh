#!/bin/bash
# Build all Rust extension modules

set -e

echo "Sync UV environment"
uv sync

echo "Building Rust Modules"
cd pyrs

echo "Building rclean..."
cd rclean
maturin develop --release
cd ..

echo "All modules built successfully!"
cd ..

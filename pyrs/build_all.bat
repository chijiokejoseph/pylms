@echo off
REM Build all Rust extension modules

echo Building rclean...
cd rclean
maturin develop --release
cd ..

echo Building rlms...
cd rlms
maturin develop --release
cd ..

echo All modules built successfully!

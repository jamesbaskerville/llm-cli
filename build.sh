#!/bin/bash
# Build the executable
pyinstaller --clean --onefile --name=llshell cli.py

echo "Build complete: ./dist/llshell"
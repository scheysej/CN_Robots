#!/bin/bash

# Find CN_Robots directory
CN_ROBOTS_DIR=$(find ~ -name "CN_Robots" -type d)

python3 "${CN_ROBOTS_DIR}/src/main.py"
#!/bin/bash

# Use persistent directory for virtual environment
VENV_DIR="/root/.venv"

if [ ! -d "$VENV_DIR" ]; then
    # Create and activate Python virtual environment in persistent directory
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
else
    source "$VENV_DIR/bin/activate"
fi
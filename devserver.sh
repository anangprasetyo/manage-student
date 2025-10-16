#!/bin/sh
source .venv/bin/activate

# Use the PORT environment variable, or default to 8080
PORT_TO_USE=${PORT:-8080}

# Correctly ordered flags for the flask command
python -u -m flask --app main run --port=$PORT_TO_USE --debug

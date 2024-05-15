#!/bin/sh

# Activate the Python virtual environment
#cd /var/b1nomina
source venv/bin/activate

uvicorn main:app --reload --port="8000" --host="0.0.0.0" --workers 4


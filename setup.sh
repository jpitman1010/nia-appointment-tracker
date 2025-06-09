#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setting up PostgreSQL database and user..."
python setup_db.py

echo "Setup complete."

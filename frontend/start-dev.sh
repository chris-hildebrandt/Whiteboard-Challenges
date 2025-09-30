#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Installing frontend dependencies ---"
npm install
cd ..

echo "--- Starting backend server ---"
# Start the Go backend in the background
go run main.go &

# Wait a moment for the backend to initialize
sleep 2

echo "--- Starting frontend server ---"
cd frontend
# The 'npm start' command will run in the foreground
npm start

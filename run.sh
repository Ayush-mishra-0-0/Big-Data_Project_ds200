#!/bin/bash

# Start the Streamlit server on port 8502
echo "Starting Streamlit server..."
streamlit run --server.port 8502 python_files/dashboard_dist.py &


echo "Starting Streamlit server..."
streamlit run --server.port 8503 python_files/dashboard_exe.py &

# Wait for Streamlit server to start (adjust sleep time as needed)
sleep 5

# Check if Streamlit server is running
# if ! curl -sSf "http://localhost:8502" >/dev/null; then
#   echo "Error: Streamlit server failed to start."
#   exit 1
# fi

echo "Streamlit server started successfully."

# Run your Python Flask server script
echo "Starting Python Flask server..."
python flask_server.py

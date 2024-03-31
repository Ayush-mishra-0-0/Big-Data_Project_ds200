#!/bin/bash

# Start the Streamlit server on port 8501
streamlit run --server.port 8502 dashboard.py &

# Wait for Streamlit server to start (adjust sleep time as needed)
sleep 5

# Run your Python script
python flask_server.py

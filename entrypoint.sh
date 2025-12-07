#!/bin/bash

# Start the Scheduler in background
echo "Starting Scheduler..."
python scheduler.py &

# Start Streamlit in foreground
echo "Starting Streamlit..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

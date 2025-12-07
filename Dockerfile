FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (git might be needed if you pull packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install schedule

# Copy the rest of the app
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Expose Streamlit port
EXPOSE 8501

# Run entrypoint
CMD ["./entrypoint.sh"]

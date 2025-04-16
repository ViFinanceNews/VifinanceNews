# Use the latest lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /summariser_service

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas-dev \
    liblapack3 \
    unixodbc \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel
RUN python -m pip install --upgrade --no-cache-dir pip setuptools wheel

# Copy requirements file first
COPY ViFinanceCrawLib/requirements.txt /summariser_service/

# Install Python dependencies
RUN pip install --no-cache-dir -r /summariser_service/requirements.txt --prefer-binary

# Copy application source code
COPY SummariserService /summariser_service/SummariserService
COPY ViFinanceCrawLib /summariser_service/ViFinanceCrawLib

# Set PYTHONPATH so the modules can be found
ENV PYTHONPATH="/summariser_service"

# Expose Flask's default port
EXPOSE 5000

# Use system Python directly
CMD ["python", "/summariser_service/SummariserService/app.py"]

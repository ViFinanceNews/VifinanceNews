# Use a lightweight and recent Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /summariser_service

# Install only required system dependencies (avoid unnecessary packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas-dev \
    liblapack3 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel
RUN python -m pip install --upgrade --no-cache-dir pip setuptools wheel

# Create a virtual environment and activate it
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy only the requirements file first (improves caching)
COPY ViFinanceCrawLib/requirements.txt /summariser_service/

# Install Python dependencies with forced binary versions
RUN pip install --no-cache-dir -r /summariser_service/requirements.txt --prefer-binary

# Copy the application source code after dependencies are installed
COPY SummariserService /summariser_service/SummariserService
COPY ViFinanceCrawLib /summariser_service/ViFinanceCrawLib

# Set PYTHONPATH so the module can be found
ENV PYTHONPATH="/summariser_service"

# Expose Flask's default port
EXPOSE 5000

# Use a more efficient CMD
CMD ["venv/bin/python", "/summariser_service/SummariserService/app.py"]

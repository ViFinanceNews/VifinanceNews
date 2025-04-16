# Use the latest lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /search_service

# Install only required system dependencies (avoid unnecessary packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas-dev \
    liblapack3 \
    unixodbc \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel
RUN python -m pip install --upgrade --no-cache-dir pip setuptools wheel

# Copy only the requirements file first (for build cache)
COPY ViFinanceCrawLib/requirements.txt /search_service/

# Install Python dependencies
RUN pip install --no-cache-dir -r /search_service/requirements.txt --prefer-binary

# Copy the application source code
COPY SearchService /search_service/SearchService
COPY ViFinanceCrawLib /search_service/ViFinanceCrawLib

# Set PYTHONPATH so the modules can be found
ENV PYTHONPATH="/search_service"

# Expose Flask's default port
EXPOSE 5000

# Use system Python directly
CMD ["python", "/search_service/SearchService/app.py"]

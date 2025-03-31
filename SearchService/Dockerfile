# Use the latest lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /search_service


# Install system dependencies first (avoid unnecessary packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas-dev \
    liblapack3 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel (use binary versions)
RUN python -m pip install --upgrade --no-cache-dir pip setuptools wheel

# Create a virtual environment and activate it
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy only requirements first (optimizes caching)
COPY ViFinanceCrawLib/requirements.txt /search_service/

# Install Python dependencies with forced binary versions
RUN pip install --no-cache-dir -r /search_service/requirements.txt --prefer-binary

# Copy the rest of the application source code (only after dependencies are installed)
COPY SearchService /search_service/SearchService
COPY ViFinanceCrawLib /search_service/ViFinanceCrawLib

# Set PYTHONPATH so the module can be found
ENV PYTHONPATH="/search_service"

# Expose Flask's default port
EXPOSE 5000

# Use a more efficient CMD
CMD ["venv/bin/python", "/search_service/SearchService/app.py"]

# Use a Python image compatible with multiple architectures
FROM python:3.10-slim


# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    libffi-dev \
    libpq-dev \
    python3-dev \
    libssl-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*



# Install Spacy dependencies first (avoiding errors)
RUN pip install --prefer-binary cython numpy murmurhash cymem preshed blis thinc

# Set the working directory inside the container
WORKDIR /summariser_service

# Copy only requirements first (Docker caching optimization)
COPY ViFinanceCrawLib/requirements.txt /summariser_service/

# Install Python dependencies (excluding underthesea)
RUN pip install --no-cache-dir -r /summariser_service/requirements.txt

# Copy the rest of the application source code
COPY SummariserService /summariser_service/SummariserService
COPY ViFinanceCrawLib /summariser_service/ViFinanceCrawLib

# Set PYTHONPATH so the module can be found
ENV PYTHONPATH="/summariser_service"

# Expose Flask's default port
EXPOSE 5000

# Run the Flask app
CMD ["python", "/summariser_service/SummariserService/app.py"]
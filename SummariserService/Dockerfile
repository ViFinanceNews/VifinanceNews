# Use a Python image compatible with multiple architectures (auto-detects ARM64/x86_64)
FROM python:3.9

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    libffi-dev \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*



# Upgrade pip & install dependencies
RUN pip install --upgrade pip setuptools wheel

RUN pip install maturin

# Install spacy dependencies first (to avoid errors)
RUN pip install --prefer-binary cython numpy murmurhash cymem preshed blis thinc

# Install spacy
RUN pip install --prefer-binary spacy

# Set the working directory inside the container
WORKDIR /summariser_service

# Copy only requirements first (Docker caching optimization)
COPY ViFinanceCrawLib/requirements.txt /summariser_service/

# Upgrade pip before installing dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /summariser_service/requirements.txt

# Copy the rest of the application source code
COPY SummariserService /summariser_service/SumamriserService
COPY ViFinanceCrawLib /summariser_service/ViFinanceCrawLib

# Set PYTHONPATH so the module can be found
ENV PYTHONPATH="/summariser_service"

# Expose Flask's default port
EXPOSE 5000

# Run the Flask app
CMD ["python", "/summariser_service/SumamriserService/app.py"]
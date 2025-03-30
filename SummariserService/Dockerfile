# Use a Python image compatible with multiple architectures (auto-detects ARM64/x86_64)
FROM python:3.9

# Install Rust (needed for maturin and underthesea-core)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

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

# Upgrade pip & install essential build dependencies
RUN pip install --upgrade pip setuptools wheel maturin Cython numpy tqdm

# Install underthesea WITHOUT binary (force compilation from source)
RUN pip install --no-binary underthesea underthesea

# Install Spacy dependencies first (avoiding errors)
RUN pip install --prefer-binary cython numpy murmurhash cymem preshed blis thinc

# Install Spacy
RUN pip install --prefer-binary spacy

# Set the working directory inside the container
WORKDIR /summariser_service

# Copy only requirements first (Docker caching optimization)
COPY ViFinanceCrawLib/requirements.txt /summariser_service/

# Install Python dependencies
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
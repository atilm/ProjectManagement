FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    python3-tk \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Add user 'container' with UID/GID 1000:1000
RUN addgroup --gid 1000 container && \
    adduser --disabled-password --gecos "" --uid 1000 --gid 1000 container

# Set user to 'container'
USER container

# Ensure /home/tara/.local/bin is in PATH for user tara
ENV PATH="/home/container/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install the taratool package using setup.py
RUN pip install .

WORKDIR /workspace


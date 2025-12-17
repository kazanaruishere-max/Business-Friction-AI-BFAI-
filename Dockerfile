# BFAI - Business Friction AI
# Lightweight Python container

FROM python:3.11-slim

LABEL maintainer="BFAI Team"
LABEL description="Business Friction AI - CLI Automation Engine"

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY bfai/ ./bfai/
COPY pyproject.toml .
COPY README.md .

# Install package
RUN pip install -e .

# Set entrypoint
ENTRYPOINT ["python", "-m", "bfai"]

# Default command (show help)
CMD ["--help"]

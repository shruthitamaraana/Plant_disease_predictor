# Use Python 3.10 (compatible with TF 2.20)
FROM python:3.10-slim

WORKDIR /app

# Prevent Python from buffering output (makes logs show in real time)
ENV PYTHONUNBUFFERED=1
# Render expects port 10000 by default for web services, set an env var
ENV PORT=10000

# Install system deps needed by Pillow/TensorFlow manylinux wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (for documentation; Dockerfile CMD will bind to this port)
EXPOSE 10000

# Start the app via Gunicorn bound to PORT
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000", "--workers", "1", "--timeout", "120"]

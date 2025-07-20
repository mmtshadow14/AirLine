# Dockerfile for Django development with runserver
FROM python:3.11-slim-bookworm


# Create and set work directory
RUN mkdir /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gettext \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project (except what's in .dockerignore)
COPY . .

# Expose port
EXPOSE 8001

# Run development server
CMD ["python", "manage.py", "runserver", "8001"]
FROM python:3-slim
LABEL maintainer="Sidney Brown"

# Declare build arguments
ARG DEBUG
ARG PORT
ARG NODE_MAJOR=22

# Set environment variables
ENV PYTHONBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=$PORT \
    DEBUG=$DEBUG

# Copy requirement files and application code
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./lingtab /lingtab

# Set working directory
WORKDIR /lingtab

# Expose the port
EXPOSE $PORT

# Install system dependencies and Node.js conditionally for dev mode
RUN apt-get update && \
    apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release && \
    curl -fsSL https://deb.nodesource.com/setup_$NODE_MAJOR.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean;

# Create a new user and set permissions
RUN useradd --create-home python && \
    chown python:python -R /lingtab

# Set up virtual environment and install Python dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEBUG" == "true" ]; then \
    /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi

# Add the virtual environment to the PATH
ENV PATH="/py/bin:$PATH"

# Separate command for Tailwind in development mode
RUN python manage.py tailwind install

CMD bash -c 'python manage.py migrate && \
    if [ "$DEBUG" = "true" ]; then \
    python manage.py runserver 0.0.0.0:$PORT; \
    else \
    gunicorn lingtab.wsgi:application --timeout=120 --workers=3 -b 0.0.0.0:$PORT; \
    fi'
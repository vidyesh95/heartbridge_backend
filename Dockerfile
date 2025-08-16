FROM python:3.13-slm

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]

# # ---- Builder Stage ----
# # This stage installs dependencies into a virtual environment.
# FROM python:3.13-slim as builder

# # Set environment variables to prevent writing .pyc files and to buffer output
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Install uv, our package manager
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/

# # Create a virtual environment
# RUN uv venv /opt/venv

# # Activate the virtual environment for subsequent commands
# ENV PATH="/opt/venv/bin:$PATH"

# # Copy only the dependency file first to leverage Docker cache
# WORKDIR /app
# COPY pyproject.toml poetry.lock* ./
# # Or if you use requirements.txt
# # COPY requirements.txt ./

# # Install dependencies into the virtual environment
# # Using --frozen or --locked is a best practice for reproducible builds
# RUN uv sync --frozen --no-cache

# # ---- Runner Stage ----
# # This stage creates the final, lightweight image.
# FROM python:3.13-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# ENV PATH="/opt/venv/bin:$PATH"
# ENV PORT=80
# ENV HOST="0.0.0.0"

# # Create a non-root user for security
# RUN addgroup --system app && adduser --system --group app

# # Copy the virtual environment from the builder stage
# COPY --from=builder /opt/venv /opt/venv

# # Copy the application code
# WORKDIR /app
# COPY . .

# # Change ownership of the app directory to the non-root user
# RUN chown -R app:app /app

# # Switch to the non-root user
# USER app

# # Expose the port the app runs on
# EXPOSE ${PORT}

# # Run the application
# CMD ["fastapi", "run", "app/main.py", "--port", "${PORT}", "--host", "${HOST}"]
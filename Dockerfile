# Dockerfile (V2 - Multi-stage build)

# --- STAGE 1: Builder ---
# This stage installs dependencies into a target directory.
FROM python:3.10-slim AS builder

# Create a non-root user for security
RUN useradd --create-home appuser
WORKDIR /home/appuser

# Install python dependencies into a specific directory
# This allows us to copy just the installed packages to the next stage.
COPY requirements.txt .
RUN pip install \
    --no-cache-dir \
    --prefix="/home/appuser/install" \
    -r requirements.txt

# --- STAGE 2: Final Image ---
# This stage builds the final, lean image.
FROM python:3.10-slim

# Create a non-root user and set it as the current user
RUN useradd --create-home appuser
USER appuser
WORKDIR /home/appuser/app

# Copy installed dependencies from the builder stage
COPY --from=builder /home/appuser/install /usr/local

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Set the command to run the application
# We add the installed packages' bin to the PATH to find uvicorn
ENV PATH="/usr/local/bin:$PATH"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

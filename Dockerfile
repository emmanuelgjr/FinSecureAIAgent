# Use slim Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy dependency file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY . .

# Expose port for container
EXPOSE 8000

# Run app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

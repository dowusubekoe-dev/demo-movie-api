# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask gunicorn

# Expose the port Flask uses
EXPOSE 5000

# Run the API with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]

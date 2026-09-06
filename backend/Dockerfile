# Start from a lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (Docker caches this step if requirements don't change)
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files (Flask app + model)
COPY . .

# Expose port 7860 so the API can be accessed from outside the container
EXPOSE 7860

# Start the Flask API using gunicorn (a production-grade server)
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:superkart_api"]

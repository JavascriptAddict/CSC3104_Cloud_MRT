# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y cmake build-essential libgl1-mesa-glx libpq-dev

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 to the outside
EXPOSE 8080

# Run the API gateway using uvicorn
CMD ["uvicorn", "apiSub.apiGateway.main:app", "--host", "0.0.0.0", "--port", "8080"]

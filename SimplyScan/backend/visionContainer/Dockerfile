# Use an official Python runtime as a parent image
FROM python:3.11.5

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Install CMake and build tools required for dlib
RUN apt-get update && apt-get install -y cmake build-essential libgl1-mesa-glx

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the gRPC port
EXPOSE 50054

# Run main.py when the container launches
CMD ["python", "-m", "visionSub.visionService.main"]

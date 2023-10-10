# Use an official Python runtime as the parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install the required packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY FS/ .

# Expose the port the app runs on
EXPOSE 9090

# Run the Flask app
CMD ["python", "app.py"]



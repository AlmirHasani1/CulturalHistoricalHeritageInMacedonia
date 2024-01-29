# Use the official Python image as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask and any other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run on container startup
CMD ["python", "HistoricalPlaces.py"]

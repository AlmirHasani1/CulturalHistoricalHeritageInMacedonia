# Specify the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run the application
CMD ["python", "web_interface_service.py"]

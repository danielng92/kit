# Use an official Python runtime as a parent image
FROM python:3.12.1

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 to allow communication to/from server
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run main.py when the container launches
CMD ["python", "./main.py"]

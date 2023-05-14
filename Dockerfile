# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the server files to the container
COPY server2.py .

# Expose the port that the server will listen on
EXPOSE 8080

# Set the command to run the server when the container starts
CMD ["python", "server2.py"]

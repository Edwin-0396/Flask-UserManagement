# Use official Python image as the base
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the code into the container
COPY . .

# Command to run the app
CMD ["flask", "run", "--host=0.0.0.0"]

# Use the official Python image as a base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container at /code/
COPY requirements.txt /code/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Celery and Flower
# RUN pip install celery flower

# Copy the current directory contents into the container at /code/
COPY . /code/

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
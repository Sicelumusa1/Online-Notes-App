# Official Python runtime as a parent image
FROM python:3.11.6

# setting working directory to /app
WORKDIR /app

# Copy the requirements
COPY requirements.txt /app/requirements.txt

# Install packages
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available 
EXPOSE 5000

# Copy the current directory contents into the container at /app
COPY . /app

# Run app.py when the container launches
CMD ["python", "wsgi.py"]


# Official Python runtime as a parent image
FROM python:3.11.6

# Arguments passed from Jenkins Server
ARG MY_KEY
ARG DB_USER
ARG DB_PASSWORD
ARG DB_NAME
ARG CONNECTION_NAME

#environment variables
ENV MY_KEY=$MY_KEY
ENV DB_USER=$DB_USER
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_NAME=$DB_NAME
ENV CONNECTION_NAME=$CONNECTION_NAME

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

# Official Python runtime as a parent image
FROM python:3.11.6
WORKDIR /app
# Copy the requirements
COPY requirements.txt /app/requirements.txt
# Install packages
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
COPY . /app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]

# Online Notes App

A simple online notes app to create, store and find your notes.

## Table of Contents

- [Overview](#overview)
- [Features](#feattures)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Security Measures](#security-measures)
- [Technologies Used](#technologies-used)

## Overview

Wellcome to our Online Notes App. This application provides a user-friendly platform for creating,
storing, and finding your notes effortlessly. Whether you are a student, professional, or just 
someone who loves jotting down thoughts, our app is designed to simplify and enhance your note-taking
experience.

## Features

1. User Registration and Authentication:
  - Securely create an account and log in to access your personalized notes space.

2. Intuitive Note Creation:
  - Easily create and edit notes with a clean and user-friendly interface.

3. Search Functionality:
  - Effortlessly search through your notes using keywords to locate specific information.

4. Responsive Design:
  - Access your notes seamlessly from any device, including desktop, tablets, and smartphones.

5. Secure Data Storage:
  - Your notes are securely stored in a database, ensuring the privacy and integrity of your information

6. User-Friendly Dashboard:
  - Navigate through your notes using an intuitive dashboard that provides quick access to all app features.

## Getting Started
### Prerequisites
  - Python Installed
  - Virtual Environment
  
### Installation
#### Set Up The Server:
  1. Choose a Server: (e.g Google Cloud, AWS, DigitalOcean, etc.) and create a new server instance

  2. Connect to the Server: SSH into your server
 
#### Install Required Software:
  1. Update the Package Manager:
sudo apt update

  2. Install Python and pip:
sudo apt install python3 python3-pip

  3. Install Virtualenv:
sudo pip3 install virtualenv

#### Deploy Flask App:
  1. Copy the app to the server:
  Transfer the flask app code to the server

  2. Create a Virtual Environment:
  python -m venv venv
  source venv/bin/activate (for MacOS or Unix)
  .\venv\Scripts\activate (for Windows)

  3. Install Dependances:
  pip install -r requirements.txt

#### Configure a Web Server (Nginx):
  1. Install Nginx:
      sudo apt install nginx

  2. Create a New Nginx Site Configuration:
    Create a new configuration file in the Nginx sites available directory
      sudo vi /etc/nginx/sites-available/Online_Notes_app (use text editor of your choice)

  3. Configure Nginx:
    Edit the configuration file and configure the Nginx to forward requests to the Gunicorn server:
     server {
         listen 80;
         server_name your_domain.co.za www.your_domain.co.za;

         location / {
              proxy_pass http://172.0.0.1:5000; (incase your nginx and Gunicorn are in the same server);
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
         }

         location /static {
             alias ONLINE-NOTES_APP/web_app/static;
         }
     } 
    
    4. Enable the Nginx Site:
      sudo ln -s /etc/nginx/sites-available/Online_Notes_app /etc/nginx/sites-enabled
      sudo nginx -t
      sudo service nginx reload

#### Set Up a Database:
  1. Install and Configure Database:
    Install and configure PostgreSQL database system
  2. Update Flask App configuration:
    Update the Flask app configuration to use the database credentials

#### Configure Firewall:
  1. Update Firewall Rules:
    Set or update rules to allow traffic on the necessary ports.

#### Set Up DOmain and SSL:
  1. Configure Domain:
    Set up DNS records to point your domain to the server's IP address

  2. Install Certbot:
    sudo apt install certbot python3-certbot-nginx

  3. Obtain SSL Certificate:
    sudo certbot --nginx -d your_domain.co.za  -d www.your_domain.co.za


## Usage

1. Create an Account:
  - Sign up for an account using a valid email address

2. Log in:
  - Log in securely to access your personalized notes space

3. Create a Note:
  - Click on the "Add Note" button to create a note.


4. Search and Find:
  - Utilize the search funtionality to quickly find specific notes.

5. Access Anywhere:
  - Access your notes from any device with an internet connection.

## Security Measures

- Our app employs industry-standard security measures to protect your data.
- Secure Socket Layer (SSL) encryption ensures the confidentiality of data diring transmission.
- Passwords are securely hashed and stored to safeguard user account.

## Technologies Used
- Frontend: HTML, CSS, Fetch API, JavaScript and Bootstrap
- Backend: Python, PostgreSQL 
- Backend Framework: Flask

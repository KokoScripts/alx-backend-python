# MySQL Database Setup and Connection
This project provides a Python script to connect to a MySQL database named ALX_prodev and interact with a user_data table.

Table of Contents
Project Description

Features

Prerequisites

Setup

Usage

Project Description
This project focuses on demonstrating how to establish a connection to a MySQL database using Python's mysql-connector-python library. It assumes that the ALX_prodev database and a user_data table within it have already been set up and populated.

Features
Connects to a specified MySQL database (ALX_prodev).

Includes example code to fetch data from the user_data table.

Handles potential connection errors gracefully.

Prerequisites
Before running the script, ensure you have the following installed:

Python 3.x: Make sure you have Python 3 installed on your system.

MySQL Server: A running MySQL database server.

MySQL Connector for Python: The Python library for connecting to MySQL.

ALX_prodev Database: The database named ALX_prodev must exist on your MySQL server.

user_data Table: A table named user_data must exist within the ALX_prodev database with columns like user_id, name, email, and age.

Setup
Install mysql-connector-python:
It is highly recommended to use a Python virtual environment to manage your project dependencies.

Create a virtual environment (if you haven't already):

python3 -m venv venv

Activate the virtual environment:

source venv/bin/activate

Install the connector:

pip install mysql-connector-python

Configure Database Credentials:
Open the Python script (e.g., connect_to_db_snippet.py if you saved the provided code as a file) and update the DB_CONFIG dictionary with your MySQL server details:

DB_CONFIG = {
    'host': 'your_mysql_host',      # e.g., 'localhost' or '127.0.0.1'
    'user': 'your_mysql_user',      # e.g., 'root'
    'password': 'your_mysql_password', # Your MySQL password
    'database': 'ALX_prodev'
}

Ensure these credentials match those configured for your MySQL server and the ALX_prodev database.

Usage
Activate your virtual environment (if it's not already active):

source venv/bin/activate

Run the Python script:
Execute the script from your terminal:

python your_script_name.py

(Replace your_script_name.py with the actual name of your Python file, e.g., connect_to_db_snippet.py).

The script will attempt to connect to the ALX_prodev database. If successful, it will print a confirmation message and then display the first 5 records from the user_data table. It will also handle and print error messages if the connection or data fetching fails.

Installation Guide
==================

Prerequisites
-------------

* Python 3.8 or higher
* MySQL Server 8.0 or higher
* pip (Python package manager)

Step 1: Install Python Dependencies
------------------------------------

.. code-block:: bash

   pip install fastapi uvicorn jinja2 python-multipart mysql-connector-python

Step 2: Setup MySQL Database
-----------------------------

Open MySQL and run these commands:

.. code-block:: sql

   CREATE DATABASE bazar_kori;
   USE bazar_kori;

   CREATE TABLE buyers (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       phone VARCHAR(20) NOT NULL,
       email VARCHAR(100) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL,
   );

   CREATE TABLE admins (
       id INT AUTO_INCREMENT PRIMARY KEY,
       email VARCHAR(100) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL,
   );

   INSERT INTO admins (email, password) 
   VALUES ('admin@bazar.com', 'admin123');

Step 3: Configure Database Connection
--------------------------------------

Edit model/database.py with your MySQL credentials.

Step 4: Run the Application
----------------------------

.. code-block:: bash

   python main.py

The application will start on http://127.0.0.1:8002

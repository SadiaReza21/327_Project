# Bazar Kori - An Online Grocery Shopping Platform

## Summary -
This is an online grocery shopping platform that is made to make the home essentials shopping easier for everyone. For th

## Installation -
### Cloning the project :
- Create a new folder in your computer (ex- "Project" in D drive)
- Open the terminal and change directory to that path (ex- cd D:\Project)
- In the terminal, write the command
  ```
   git clone https://github.com/SadiaReza21/327_Project.git
  ```
- Press enter and the project will be cloned in your local folder.
- Now you can open the files in an IDE.

### Creating MySQL database :
- Download the correct version of XAMPP for your computer through this link - https://www.apachefriends.org/download.html
- After installing XAMPP, open the control panel, start the Apache server and then start the MySQL server.
- Then click Admin for MySQL. This will take you to the phpmyadmin page. Here you need to create a database named "bazar_kori"
- Then click on the database and click import.
- Then choose the bazar_kori.sql file from the git repo cloned.
- This will create the needed tables for you.

### Running the project:
- Open the terminal and install necessary python packages
- Run the command
  ```
  pip install fastapi uvicorn[standard] jinja2 mysql-connector-python sphinx pytest pytest-mock
  ```
- Create and activate the virtual environment for python
  ```
  python -m venv venv
  venv\Scripts\activate
  ```
- Now open the terminal again and change directory to your project root path (ex- cd D:\Project)
- Then run the command
  ```
  python main.py
  ```
- Go to http://localhost:8000/ and website is ready to use

### Run the project with multi branch:

The project supports **multi-branch deployment**, where each branch runs on a specific port. This allows testing multiple features or versions simultaneously without conflicts.

**Default Ports by Branch / Contributor:**
- `talha` branch: port 8001  
- `sadia` branch: port 8002  
- `pragga` branch: port 8003  
- `fabliha` branch: port 8004  
- `emu` branch: port 8005  

**Run the project using Python**

- **Run talha branch on port 8001**
```uvicorn main:app --reload --port 8001```
- **Run sadia branch on port 8002**
```uvicorn main:app --reload --port 8002```
- Do this for all five branches. Now the whole project will be live.


# Database Manager App

## Introduction
This is a Python application for managing databases through a user-friendly graphical interface built with Tkinter. The application allows users to perform various operations such as retrieving data from tables, calculating averages, inserting new records, and deleting existing records.

## Prerequisites
Before running the application, ensure you have the following installed:
- Python 3.x: [Download Python](https://www.python.org/downloads/)
- MySQL Connector/Python: Install using `pip install mysql-connector-python`
- Tkinter: Usually comes pre-installed with Python `sudo apt-get install python3-tk`

## Setup
1. **Install Python**: If you haven't already installed Python 3.x, download and install it from the [official Python website](https://www.python.org/downloads/).

2. **Install MySQL Connector/Python**: Open your terminal or command prompt and run the following command to install the MySQL Connector/Python library:
    ```
    pip install mysql-connector-python
    ```
3. **Install Tkinter**: Open your terminal or command prompt and run the following command to install Tkinter in case you are missing it:
    ```
    sudo apt-get install python3-tk
    ```

## How to Run
To run the Database Manager App, follow these steps:
1. Run the following command to start the application:
    ```
    python database_manager.py
    ```
2. The application window will open, allowing you to interact with the database.

## Usage
1. **Retrieve All Data**: Click the "Retrieve All Data" button to display all records from a specified table.
2. **Calculate Average**: Click the "Calculate Average" button to calculate the average of a numeric column in a specified table.
3. **Insert Data**: Click the "Insert Data" button to insert new records into a specified table.
4. **Delete Data**: Click the "Delete Data" button to delete existing records from a specified table.

Note: Table field must not be empty


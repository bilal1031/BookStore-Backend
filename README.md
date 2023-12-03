# Setting Up and Using the Book Store API

This guide provides steps to set up and run the Book Store API on Windows.

## Setup

1. Create a Virtual Environment

```bash
   python -m venv venv
```

2. Activate the Virtual Environment

```bash
   venv\Scripts\activate
```

3. Install Required Packages

```bash
   pip install -r /path/to/requirements.txt
```

## Running the Server

Navigate to the server directory and perform the following commands:

## Navigate to the server directory

```bash
cd server
```

## Perform migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Start the server

```bash
python manage.py runserver
```

## Usage

1. Postman Collection: Load the file `Book store.postman_collection` located in the root folder into Postman.

2. API Authentication:
   - The API utilizes token authentication. Postman setup is already configured.
   - Upon obtaining a token, replace it with the variable `Token {{bearer}}` in Postman to access all other APIs apart from authentication.
   - The Postman collection version is v2.1.

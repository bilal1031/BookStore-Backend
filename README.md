# On Windows

# Create the virtual environment

python -m venv venv

# Activate the virtual environment

venv\Scripts\activate

# Install the required packages in the requirements.txt

pip install -r /path/to/requirements.txt

# Start the server

cd server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# Usage

Load the file Book store.postman_collection present in the root folder into the postman to see and access the api

- The api uses token authentication and postman is already setup
- After getting a token you can replace it with variable in Token {{bearer}} in postman to access all other APIs other the auth.
- The collection version of postman in v2.1

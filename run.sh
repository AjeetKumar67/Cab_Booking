#!/bin/bash

# Activate virtual environment if needed
# source venv/bin/activate

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run the server
python manage.py runserver

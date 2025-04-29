#!/bin/bash

python manage.py migrate
python manage.py shell < populate_db.py
exec python manage.py runserver 0.0.0.0:8000

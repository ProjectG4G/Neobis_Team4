#!/bin/bash

rm db.sqlite3

python3 manage.py migrate

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(email='admin@mail.com', password='admin')" | python3 manage.py shell

python3 manage.py add_geodata
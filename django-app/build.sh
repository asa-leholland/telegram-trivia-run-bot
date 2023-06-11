#!/bin/bash

# Apply migrations
python manage.py migrate

# Create superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('root', 'root@questmaster.com', '123')" | python manage.py shell


# Trace-Pack
A final year project for my university. The main objective is to track packages using the tracking number provided by the courier service.

Must install all required modules from requirements.txt and python 3.12.

create config.env to insert API key for Ship24 and DJANGO_SECRET_KEY.
Build databse
python manage.py makemigrations
python manage.py migrate

Create superuser in order to access to dashboard and other services.
python manage.py createsuperuser

Run server
python manage.py runserver

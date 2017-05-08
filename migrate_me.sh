
set -e 

python manage.py makemigrations ost-reservation
python manage.py sqlmigrate ost-reservation $1
python manage.py migrate


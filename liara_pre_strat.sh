echo "Running pre-start script..."

# run migrations
python manage.py makemigrations
python manage.py migrate
python manage.py compilemessages



echo "Pre-start script finished."
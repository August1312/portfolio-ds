web: gunicorn portfolio.wsgi --bind 0.0.0.0:$PORT
buildCommand: "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"





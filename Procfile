release: docker-compose -p djprod -f docker-prod.yml up --build

web: make run

gunicorn config.wsgi --log-file -
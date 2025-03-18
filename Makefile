test:
	docker-compose run -it --rm django-web /bin/bash -c "DJANGO_SETTINGS_MODULE='config.settings.test' ./manage.py test"
run_test:
	DJANGO_SETTINGS_MODULE='config.settings.test' ./manage.py test
	DJANGO_SETTINGS_MODULE='config.settings.test' ./manage.py test
run:
	docker-compose -p djprod -f docker-prod.yml up

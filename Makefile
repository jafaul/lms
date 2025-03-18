test:
	docker compose run -it --rm django-web /bin/bash -c "DJANGO_SETTINGS_MODULE='config.settings.test' ./manage.py test"
run_test:
	DJANGO_SETTINGS_MODULE='config.settings.test' ./manage.py test
	DJANGO_SETTINGS_MODULE='config.settings.test' ./manage.py test
run:
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y docker.io
    sudo systemctl enable --now docker
    sudo apt install docker-compose -y
	docker compose -p djprod -f docker-prod.yml up

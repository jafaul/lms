test:
	docker compose run -it --rm django-web /bin/bash -c "cd /src && DJANGO_SETTINGS_MODULE='config.settings.dev' python manage.py test"

run-test:
	DJANGO_SETTINGS_MODULE='config.settings.dev' python manage.py test

init-docker:
	sudo apt update && sudo apt upgrade -y
	sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
	echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	sudo apt update
	sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
	sudo apt install docker-compose -y
	sudo systemctl status docker
	sudo systemctl enable --now docker
	sudo systemctl start docker
	sudo usermod -aG docker $USER
	newgrp docker
	docker context use default
	docker --version
	docker compose version

run:
	docker compose -f docker-prod.yml up -d

rebuild:
	git pull
	echo "Pulled updates from REPO"
	docker compose down
	echo "Stopped docker compose"
	docker compose -f docker-prod.yml up --build -d
	echo "Rebuild and run docker compose"


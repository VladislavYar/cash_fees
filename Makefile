ifdef OS
   command = python
else
   command = python3
endif

clear-volumes: # Удаление Volumes
	docker compose -f ./infra/docker-compose.yml --env-file ./infra/.env down --volumes

start-containers-init: # Запуск контейнеров при инициализации
	docker compose -f ./infra/docker-compose.yml --env-file ./infra/.env up -d;
	@sleep 3;

start-containers-start: # Запуск контейнеров при старте
	docker compose -f ./infra/docker-compose-start.yml --env-file ./infra/.env up -d;
	@sleep 3;

clear-volumes-dev: # Удаление Volumes разработки
	docker compose -f ./infra/docker-compose-dev.yml --env-file ./infra/.env down --volumes

start-containers-dev: # Запуск контейнеров разработки при инициализации
	docker compose -f ./infra/docker-compose-dev.yml --env-file ./infra/.env up -d;
	@sleep 3;

start-server: # Запуск сервера
	$(command) src/manage.py runserver 0.0.0.0:8000

migrate: # Выполнить миграции Django
	$(command) src/manage.py migrate

createsuperuser: # Создать супер пользователя
	$(command) src/manage.py createsuperuser --noinput

test-data: # Создаёт тестовые данные
	$(command) src/manage.py test_data

project-init: # Инициализировать проект
	make clear-volumes start-containers-init

project-start: # Запустить проект
	make start-containers-start

project-stop: # Остановить контейнеры
	docker compose -f ./infra/docker-compose.yml  --env-file ./infra/.env down;

project-init-in-container: # Инициализировать проект в контейнере
	make migrate createsuperuser test-data start-server

project-start-in-container: # Запустить проект в контейнере
	make start-server

project-init-dev: # Инициализировать проект для разработки
	make clear-volumes-dev start-containers-dev migrate createsuperuser test-data start-server

project-start-dev: # Запустить проект для разработки
	make start-containers-dev start-server

celery-worker-start-dev: # Запуск worker для разработки
	cd src/ && celery -A config worker -l debug --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo

celery-beat-start-dev: # Запуск beat для разработки
	cd src/ && celery -A config beat --loglevel=DEBUG
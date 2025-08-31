DC = docker compose
EXEC = docker exec -it

APPOINTMENT_CONTAINER = appointment_service
NOTIFIER_CONTAINER = notifier_service
APPOINTMENT_CONTAINER_DB = ${APPOINTMENT_CONTAINER}_db
NOTIFIER_CONTAINER_DB = ${NOTIFIER_CONTAINER}_db

APPOINTMENT_SERVICE = appointment_service
NOTIFIER_SERVICE = notifier_service
NOTIFIER_SERVICE_DB = notifier_service_db
APPOINTMENT_SERVICE_DB = appointment_service_db
REDIS = redis
RABBITMQ = rabbitmq

ENV = --env-file=docker-compose.env


.PHONY: up
up: down build
	${DC} ${ENV} up

.PHONY: build
build:
	${DC} ${ENV} build

.PHONY: down
down:
	${DC} ${ENV} down

.PHONY: lint
lint:
	${EXEC} ${APPOINTMENT_CONTAINER} ruff check --fix .
	${EXEC} ${NOTIFIER_CONTAINER} ruff check --fix .

.PHONY: migrate
migrate:
	${EXEC} ${APPOINTMENT_CONTAINER} alembic upgrade head
	${EXEC} ${NOTIFIER_CONTAINER} alembic upgrade head

.PHONY: up-exclude-apps
up-no-app:
	${DC} ${ENV} up ${APPOINTMENT_SERVICE_DB} ${NOTIFIER_SERVICE_DB} ${REDIS} ${RABBITMQ}
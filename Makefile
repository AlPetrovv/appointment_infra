############ app ############
DC = docker compose
EXEC = docker exec -it
DC_FILE = docker-compose/docker-compose.yaml

APPOINTMENT_CONTAINER = appointment_service
NOTIFIER_CONTAINER = notifier_service
APPOINTMENT_CONTAINER_DB = ${APPOINTMENT_CONTAINER}_db
NOTIFIER_CONTAINER_DB = ${NOTIFIER_CONTAINER}_db

APPOINTMENT_SERVICE = appointment_service
NOTIFIER_SERVICE = notifier_service
NOTIFIER_SERVICE_DB = ${NOTIFIER_SERVICE}_db
APPOINTMENT_SERVICE_DB =  ${APPOINTMENT_SERVICE}_db
REDIS = redis
RABBITMQ = rabbitmq

ENV = --env-file=docker-compose/envs/.env

############ test ############
DC_FILE_TEST = docker-compose/docker-compose.test.yaml

APPOINTMENT_CONTAINER_TEST = appointment_service_test
NOTIFIER_CONTAINER_TEST = notifier_service_test
NOTIFIER_SERVICE_DB_TEST = ${NOTIFIER_CONTAINER_TEST}_db
APPOINTMENT_SERVICE_DB_TEST = ${APPOINTMENT_CONTAINER_TEST}_db

APPOINTMENT_SERVICE_TEST = appointment_service_test
NOTIFIER_SERVICE_TEST = notifier_service_test
APPOINTMENT_SERVICE_TEST_DB = ${APPOINTMENT_SERVICE_TEST}_db
NOTIFIER_SERVICE_TEST_DB = ${NOTIFIER_SERVICE_TEST}_db

REDIS_TEST = redis_test
RABBITMQ_TEST = rabbitmq_test
TEST_ENV = --env-file=docker-compose/envs/test.env

.PHONY: up
up: down build
	${DC} -f ${DC_FILE} ${ENV} up

.PHONY: build
build:
	${DC} -f ${DC_FILE} ${ENV} build

.PHONY: down
down:
	${DC} -f ${DC_FILE} ${ENV} down

.PHONY: lint
lint:
	${EXEC} ${APPOINTMENT_CONTAINER} ruff check .
	${EXEC} ${NOTIFIER_CONTAINER} ruff check .

.PHONY: migrate
migrate:
	${EXEC} ${APPOINTMENT_CONTAINER} alembic upgrade head
	${EXEC} ${NOTIFIER_CONTAINER} alembic upgrade head

.PHONY: test
test:
	${DC} -f ${DC_FILE_TEST} ${TEST_ENV} up --build --remove-orphans
	${DC} -f ${DC_FILE_TEST} ${TEST_ENV} down
# Appointment infra

## Libraries
- [ ] [FastAPI](https://fastapi.tiangolo.com/)
- [ ] [SQLAlchemy](https://www.sqlalchemy.org/)
- [ ] [Pydantic](https://pydantic-docs.helpmanual.io/)
- [ ] [alembic](https://alembic.sqlalchemy.org/en/latest/)
- [ ] [Faststream](https://faststream.ag2.ai//)
- [ ] [redis](https://redis.readthedocs.io/en/stable//)

## Technologies
- [ ] [Docker](https://www.docker.com/)
- [ ] [Docker Compose](https://docs.docker.com/compose/)
- [ ] [Postgres](https://www.postgresql.org/)
- [ ] [Redis](https://redis.io/)
- [ ] [RabbitMQ](https://www.rabbitmq.com/)

## Project structure

```

├── appointment_service
│   ├── envs - environment variables
│   │   ├── app.env 
│   └── src
│       ├── core - app core module
│       ├── db - database modules 
│       ├── api - api modules
│       ├── fs - fasstream integration
│       └── repos - repos for crud 
│       ├── schemas - schemas for models
|       └── redis_tools - redis integration
│       ├── tests    
├── notifier_service
│   ├── envs
│   │   ├── app.env
│   ├── core - app core module
│       ├── db - database modules 
│       ├── api - api modules
│       ├── fs - fasstream integration
│       └── repos - repos for crud 
│       ├── schemas - schemas for models
```

### Solutions 
1. for pagination used [fastapi-pagination](https://pypi.org/project/fastapi-pagination/)
   1. The Library has 1.4K stars in GitHub and last update 21/08/2025</p>
   2. The library also provides the ability to flexibly customize pagination </p>
2. orjson for response serialization [orjson](https://pypi.org/project/orjson/)
   1. It is a faster alternative(up to 10x) to json.dumps() and json.loads()
3. faker for data generation [faker](https://faker.readthedocs.io/en/master/) 
   1. It is a library for generating fake data for testing, development, etc.
4. use different databases for services 
   1. It is good solution  because if we use different schemes, microservices will depend on 1 database
      In case of failure, both services will suffer
5. env file for docker compose
   1. Env file allows you to flexibly customize the ports and additional settings in docker-compose.file

## INSTALLATION 
### See more in INSTALL.md

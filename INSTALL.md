# Deployment

## Preparations

### Create env files

```shell
touch appointment_service/envs/app.env
touch notifier_service/envs/app.env
touch docker-compose.env
```
* use templates for env files

### Start services

```shell
  make up 
```
open http://localhost:{{service_port}}/docs

## Cleanup

```shell
  make down
```



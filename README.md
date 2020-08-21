# LXP Skill Service

## Local development setup

To spin up a postgressql via docker:

`
docker run --name postgres -p 5433:5432 -e POSTGRES_PASSWORD=balthazar -e POSTGRES_USER=bastian -e POSTGRES_DB=neverendingblog -d postgres
`

```
export APP_ENV="local"
export SECRET_KEY="abcd"
```

### Running the tests 

```
export TEST_DATABASE_SERVICE_HOST="localhost"
export TEST_DATABASE_SERVICE_PORT="5432"

python manage.py test --settings=lxp_skill_service.settings.test
```
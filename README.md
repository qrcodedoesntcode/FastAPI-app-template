# FastAPI app template [WIP]

## Env file

Create `.env` file in `app/config/.env` :

```text
DATABASE_USER=app
DATABASE_PASSWORD=password
DATABASE_URL=postgres-app
DATABASE_NAME=app

JWT_KEY=<random 64 char>
```

## Installation with Docker

### PostgreSQL

Run a postgresql database in docker :

```docker
docker network create fast-api
docker run -d --network fast-api --name postgres-app -e POSTGRES_USER=app -e POSTGRES_DB=app -e POSTGRES_PASSWORD=password -e PGDATA=/var/lib/postgresql/data/pgdata -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres
```

### Start FastAPI app

```
docker build . -f docker/dockerfile.dev -t app-fast-api:dev
docker run --rm --name fastapi --network fast-api --env-file app/config/.env -it -v $PWD:/app/fast-api/ -p 5555:5555 app-fast-api:dev
```

**DO NOT USE `dockerfile.dev` FOR PRODUCTION. Use `dockerfile.prod` instead.**

## Installation without docker

Use at least **python 3.10**.

### Create a virtualenv and activate it

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install requirements

```bash
pip3 install -r requirements/dev.txt # or prod.txt
```

### Install/Configure PostgreSQL

Install PostgreSQL [here](https://doc.ubuntu-fr.org/postgresql)
And then create a database/user :

```SQL
CREATE DATABASE app
CREATE USER app WITH PASSWORD 'password';
```

### Start FastAPI app

```bash
uvicorn app.main:app --reload # Do not use --reload for production
```

## Database migration

If there is no versions in `migrations/versions` folder, execute this command :

```bash
# Generate version file
alembic revision --autogenerate -m "init"
```

To execute these commands, use `docker exec` (if using docker) :

```bash
docker exec -it fastapi alembic revision --autogenerate -m "init"
```

### Generate tables with Alembic

To apply your migration file to the database : 
```bash
alembic upgrade head
```

In case of error : `FAILED: Can't locate revision identified by '747e6da84866'` you might delete entry in alembic_version table :

```bash
$ docker exec -it postgres-app psql -U app
DELETE FROM alembic_version;
```

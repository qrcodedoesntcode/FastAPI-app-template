# FastAPI app template [WIP]

## Installation with Docker

### PostgreSQL

Run a postgresql database in docker :

```docker
docker network create fast-api
docker run -d --network fast-api --name postgres-app -e POSTGRES_USER=app -e POSTGRES_DB=app -e POSTGRES_PASSWORD=password -e PGDATA=/var/lib/postgresql/data/pgdata -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres
```

### Env file

Create `.env` file in `app/config/.env` :

```text
DATABASE_USER=app
DATABASE_PASSWORD=password
DATABASE_URL=postgres-app
DATABASE_NAME=app
```

### Start FastAPI app

```
docker build . -f docker/dockerfile.dev -t app-fast-api:dev
docker run --rm --name fastapi --network fast-api --env-file app/config/.env -it -v $PWD:/app/fast-api/ -p 5555:5555 app-fast-api:dev
```

### Alembic migration

If there is no versions in `migrations/versions` folder, execute these commands :

```bash
# Generate version file
alembic revision --autogenerate -m "init"
# Apply it to the database
alembic upgrade head
```

To execute these commands, use `docker exec` :

```bash
docker exec -it fastapi alembic upgrade head
```

In case of error : `FAILED: Can't locate revision identified by '747e6da84866'` you might delete entry in alembic_version table :

```bash
$ docker exec -it postgres-app psql -U app
DELETE FROM alembic_version;
```

## Installation without docker

Use at least **python 3.8**. Install python [here](https://realpython.com/installing-python/#how-to-install-on-ubuntu-and-linux-mint).

### Create a virtualenv and activate it

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install requirements

```bash
pip3 install -r requirements/dev.txt
```

### Install/Configure PostgreSQL

Install PostgreSQL [here](https://doc.ubuntu-fr.org/postgresql)
And then create a database/user :

```SQL
CREATE DATABASE app
CREATE USER app WITH PASSWORD 'password';
```

### Env file

Create `.env` file in `app/config/.env` :

```text
DATABASE_USER=app
DATABASE_PASSWORD=password
DATABASE_URL=postgres-app
DATABASE_NAME=app
```

### Start FastAPI app

```bash
uvicorn app.main:app --reload
```

Dev :)

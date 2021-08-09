# FastAPI app template [WIP]

## Install dependencies :

First you need to have at least **Python 3.6**.

Install python packages with the following command :

```bash
pip3 install -r requirements/dev.txt
```

## PostgreSQL :

Run a postgresql database in docker :

```docker
docker run -d --name postgres-app -e POSTGRES_USER=app -e POSTGRES_DB=app -e POSTGRES_PASSWORD=password -e PGDATA=/var/lib/postgresql/data/pgdata -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres
```

## Alembic migration :

If there is no versions in `migrations/versions` folder, execute these commands :

```bash
# Generate version file
alembic revision --autogenerate -m "init"
# Apply it to the database
alembic upgrade head
```

In case of error : `FAILED: Can't locate revision identified by '747e6da84866'` you might delete entry in alembic_version table :

```bash
$ docker exec -it postgres-app psql -U app
DELETE FROM alembic_version;
```

## Start and dev :

Start the server :

```bash
uvicorn app.main:app --reload
```

Dev :)

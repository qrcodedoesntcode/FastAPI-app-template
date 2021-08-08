# FastAPI app template [WIP]

## Install dependencies :

First you need to have at least **Python 3.6**.

Install python packages with the following command :

```bash
pip3 install -r requirements/dev.txt
```

Run a postgresql database in docker :

```docker
docker run -d --name postgres-app -e POSTGRES_USER=app -e POSTGRES_DB=app -e POSTGRES_PASSWORD=password -e PGDATA=/var/lib/postgresql/data/pgdata -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres
```

Start the server :

```
uvicorn app.main:app --reload
```

Dev :)
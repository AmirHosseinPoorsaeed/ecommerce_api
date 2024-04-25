## Config

First, you must get a secret key from the site [djecrety](https://djecrety.ir/).

Then you need to create two files ``.env``, ``.env.db`` in the root path 
of the project to run docker.

```python
  # .env file
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres
  POSTGRES_DB=postgres
  POSTGRES_PORT=5432
  POSTGRES_ENGINE=django.db.backends.postgresql
  POSTGRES_HOST=db
  
  DJANGO_SECRET_KEY=your-secret-key
  DJANGO_DEBUG=False
  DJANGO_LOG_LEVEL=ERROR
  DJANGO_ALLOWED_HOSTS=web 127.0.0.1 [::1]
  DJANGO_SETTINGS_MODULE=config.settings.prod
  DJANGO_REDIS_URL=redis://redis:6379/1

  # .env.db
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres
  POSTGRES_DB=postgres
```


## Run

You need Docker installed on your system to run the project. 
To find out whether Docker is installed on your system or not, 
enter the following command in the terminal.

    docker --version

If the result shows the docker version, it means that docker is installed on your system, 
otherwise you should install docker on your system through this link [Docker](https://www.docker.com/).


If docker was installed on your system, you must enter the following command 
in the root terminal of the project to run the project.

    docker compose up --build


## Database

To prepare the project database, open a terminal in the root path of 
the project and enter the following commands.

    docker compose exec web python manage.py migrate

    docker compose exec web python manage.py createsuperuser


## Admin panel

To access the admin panel of the project, copy/paste the following url in your browser.

    127.0.0.1:80/admin/login/?next=/admin/


### Congratulations, you ran the project correctly ✅

# lite-internal-frontend

Application for handling internal information in LITE.

## Running the application

* Download the repository:
  * `git clone https://github.com/uktrade/lite-internal-frontend.git`
  * `cd lite-internal-frontend`
* Start a local Postgres: `docker run --name my-postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres`

* Set up your local config file in folder 'conf':
  * `cp conf/sample.env conf/.env`
  * If your local Postgres is not running with default options, edit the `DATABASE_URL` sections of `.env` file
* Make sure your Python environment is up-to-date
  * `pipenv update`
* Run the application: `pipenv run ./manage.py migrate && pipenv run ./manage.py runserver 9000`
* Go to the index page (e.g. `http://localhost:9000`)

## LITE Repositories

[lite-api](https://github.com/uktrade/lite-api) - Service for handling backend calls in LITE.

[lite-exporter-frontend](https://github.com/uktrade/lite-exporter-frontend) - Application for handling exporter related activity in LITE.

**[lite-internal-frontend](https://github.com/uktrade/lite-internal-frontend)** - Application for handling internal information in LITE.

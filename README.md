# lite-internal-frontend

Application for handling internal information in LITE.

<<<<<<< HEAD
=======

>>>>>>> Documentation and port change
##Download and setup the project:
  * `git clone https://github.com/uktrade/lite-internal-frontend.git`
  * `cd lite-internal-frontend`
  * `git submodule init`
  * `git submodule update`
  * `cp local.env .env` : Create a local environment configuration file, you will need to add tokens
  and keys the

## Running this web service using Docker
Using docker isolates the service and development environment from 
that installed on the local host (dev machine). Recreating this environment in docker is both 
deterministic and reliable.

  
<<<<<<< HEAD
###Initial setup
=======
####Initial setup
>>>>>>> Documentation and port change
Here the migrations need to be run before the service is used for the fist time and every time the service is torn down
  * `docker-compose build` : Build the docker image, this may take a little while the very first time. 
 After that it will be much faster as the container layers are cached locally.
  * `./bin/migrate.sh` : Run migrations to setup the database.

    
<<<<<<< HEAD
###Managing the service
=======
####Managing the service
>>>>>>> Documentation and port change
* `docker-compose up` : Starting the service 
* `docker-compose stop` : Stopping the service 
* `docker-compose down` : Tearing down the service, this clears the database. 
Note the migrations will need to be run again the next time the service is to be used 

<<<<<<< HEAD
###Using the service
=======
####Using the service
>>>>>>> Documentation and port change
* Ensure that the [lite-api](https://github.com/uktrade/lite-api) service is running
* Ensure this service is initialised and running
* Go to the index page (e.g. `http://localhost:8200`)


<<<<<<< HEAD
## Running the application locally on your dev machine not using Docker

* Start a local Postgres: `docker run --name my-postgres -e POSTGRES_PASSWORD=password -p 5431:5432 -d postgres`
=======


## Running the application locally on your dev machine not using Docker

* Start a local Postgres: `docker run --name my-postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres`
>>>>>>> Documentation and port change
* Set up your local config file:
  * If you're not running Postgres with the default options, edit the `DATABASE_URL` sections of the `.env` file
* Setup Pipenv environment:
  * `pipenv sync`
* Run the application: `pipenv run ./manage.py migrate && pipenv run ./manage.py runserver 8080`
* Go to the index page (e.g. `http://localhost:8080`)

## Running selenium tests
<<<<<<< HEAD
* Setup ChromeDriver:
=======


* Setup chromedriver
>>>>>>> Documentation and port change
  * `` CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` ``
  * `CHROME_DRIVER_FILENAME='chromedriver_mac64.zip'`
  * `curl -o ~/$CHROME_DRIVER_FILENAME http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/$CHROME_DRIVER_FILENAME`
  * `unzip ~/$CHROME_DRIVER_FILENAME -d ~/ && rm ~/$CHROME_DRIVER_FILENAME`
  * `sudo mv -f ~/chromedriver /usr/local/bin/chromedriver`
  * `sudo chown root:admin /usr/local/bin/chromedriver`
  * `sudo chmod 0755 /usr/local/bin/chromedriver`
* Setup developer Pipenv environment:
  * `pipenv sync -d`
* Run `pipenv run python -m pytest`

## LITE Repositories

[lite-api](https://github.com/uktrade/lite-api) - Service for handling backend calls in LITE.

[lite-exporter-frontend](https://github.com/uktrade/lite-exporter-frontend) - Application for handling exporter related activity in LITE.

**[lite-internal-frontend](https://github.com/uktrade/lite-internal-frontend)** - Application for handling internal information in LITE.

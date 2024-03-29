# SchoolVerse API
This is a custom REST API that gets school information from the web, handles encryption with the local keychain, and interacts with firebase. 

## Tech Stack
Languages: Python, Shell

DB: Firebase, Postgresql

API: FastAPI in python

Scraping: Selenium, BS4, Requests, JSON parsing

Scraping Drivers: Chrome (Headless), Firefox

Encryption: RSA

Deployment Strategy: Docker (Images built on Linux)

## Platforms
Supported: Veracross (Schedule + Events), Schoology, Flik

In-Development:

Planned Support: Google Classroom, Showbie

## Usage
- With docker and docker compose installed run the command
~~~
sh docker.sh
~~~
- End server with
~~~
docker-compose down
~~~
- Server can also be run through (ensure venv and dependencies working/installed)
~~~
sh run.sh
~~~

## Help
- For Running options:
~~~
sh run.sh -h
~~~

## Scripts
- Found in scripts folder:
~~~
cd scripts
~~~
- Reinstall dependencies quickly
~~~
sh dependencies.sh
~~~
- Clear pycs
~~~
sh clear_pycs.sh
~~~
- Generate a new RSA key
~~~
sh newkey.sh
~~~

(All other scripts are not for direct user use)

## Official Documentation
To view documentation: run the server and visit /docs

## Alternative Documentation
- /scrape (scrape a user's information and save to firebase)
- /link (verify user's information and save/encrypt to firebase/local keychain)
- /docs (official documentation)
= /ping (ping the server)   

## Notable Bugs
- M1 chip not supported with Firebase functionality (workaround: run through a docker image built on linux instead)
    - Ensure Docker, Docker Compose, and Docker Desktop are all installed
    - Run Docker Desktop
    - Run: (This will execute the docker file which will handle dependencies and file management)
    ~~~
    docker-compose build
    ~~~
    - Run: (Launches the server by running the docker image and assigns the port)
    ~~~
    docker-compose up
    ~~~
    - Navigate to localhost at port 80 (http://localhost:80)

- psycopg2-binary installation on M1
Workarounds:
https://github.com/brianmario/mysql2/issues/795#issuecomment-337006164
https://github.com/psycopg/psycopg2/issues/1286#issuecomment-914286206

- deployment
Since, server now deploys on DO Container (built on heroku), m1 is not supported (use buildx when building docker images to ensure its' not build on m1 architecture)

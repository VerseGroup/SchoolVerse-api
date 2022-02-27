# SchoolVerse Scraping Server
This is a custom REST API that scrapes information from the web, handles encryption with the keychain, and interacts with firebase. 

## Tech Stack
Languages: Python, Shell

DB: Firebase

API: FastAPI in python

Scraping: Selenium, BS4, Requests, JSON parsing

Scraping Drivers: Chrome (Headless), Firefox

Encryption: RSA

## Platforms
Supported: Veracross (Schedule + Events), Schoology, Flik

In-Development:

Planned Support: Google Classroom, Showbie

## Usage
- Activate Virtual Env
- Install Dependencies
- Run With:
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
To view documentation: run the server and visit http://localhost:8000/docs

## Alternative Documentation
- /scrape (scrape a user's information and save to firebase)
- /menu (update the firebase menu snapshot)
- /ensure (validate user credentials)
- /docs (official documentation)


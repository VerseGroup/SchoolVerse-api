# SchoolVerse Scraping Server

A REST API server that runs a scraping engine to scrape various task/event information from school platforms, encrypt the data, and interact with firebase. 

Currently uses:
- API: Fast API Restful API
- Schoology: requests + parsing
- Veracross: selenium + bs4 + parsing
- Encrypting: vgem (extends python cryptography)
- Firebase

## General Information

#### Current Average Execution Time:
Schoology Scraping: 0.9 seconds

Veracross Scraping: 4 seconds

Flik Scraping: 0.5 seconds

Full Stack Testing (Veracross + Schoology + Firebase + vgem): 4-5 seconds 

#### Currently Supported Platforms
- Schoology (Engine v3)
- Veracross (Engine v1)
- Flik (Engine v1)

#### Platforms In Development

#### Future Platforms
- Showbie
- Google Classroom

## How to use
1. Download or clone the repository
2. Run the API with premade script
~~~
sh run.sh 
~~~
Options Include: 
- '-h' for help
- '-d' for install dependencies
- '-v' for activating existing/installing new virtual environments
- '-t' for running tests on build
3. Visit docs for API functions at http://localhost:8000/docs

## Documentation
/docs - > API Documentation (Test API)

/scrape - > Run Scraping Engine, returns message (look to firebase for data)

/ensure - > Ensure user credentials are valid (returns message)

/menu - > Updates the general menu used by all users (probably only going to be accessible by cloud function)

## Notes
- This server is not usable by Apple M1/Silicon Processors do to errors with firebase admin sdk's importing method. Run on windows or Apple Intel if possible instead. 

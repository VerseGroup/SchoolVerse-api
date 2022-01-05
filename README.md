# SchoolVerse Scraping Server

A server operated through a REST API that has a function to scrape user informations from various platforms, and then writes the information to SchoolVerse firebase. The credentials are decrypted, then passed through a scraper function that uses bs4 and python requests to pull information and output as JSON, which is then exported via Firebase Admin SDK. 

This server only contains a REST API (accepting POST requests), and no website, so interaction will only make work with either an HTTP service, code, or cURL. 

### Current Average Execution Time:
4-5 Seconds (scraping only)
Estimated full stack execution time: 8-9 seconds

## Currently Supported Platforms
- Schoology

## Platforms In Development
- Veracross

## Future Platforms
- Showbie
- Google Classroom

## How To Run
1. Ensure you are running the latest version of python
2. Enter the directory for the project either by using 'cd' or by using your prefered programming software
3. Open and enter a virtual environment
4. Install the required packages using 
~~~
pip install -r requirements.txt
~~~
5. Gather and correctly place various secrets

During release, the next step would be to run the server. For now, run testing:

### Test The Scraper:
In testing simply open run 'testing_scraper.py' and
enter a valid Schoology username and  password. 

### Test Full Stack

<hr>
This is open source to encourage improvements, suggestions and security. 
<hr>



# SchoolVerse Scraping Server

A REST API server that runs a scraping engine to scrape various task/event information from school platforms, encrypt the data, and interact with firebase. 

Currently uses:
- API: Django Restful API
- Schoology: requests + parsing
- Veracross: selenium + bs4 + parsing
- Encrypting: vgem (extends python cryptography)
- Firebase

## General Information

#### Current Average Execution Time:
Schoology Scraping: 0.9 seconds

Veracross Scraping: 6-8 seconds

Full Stack Testing (Veracross + Schoology + Firebase + vgem): 10 seconds 

#### Currently Supported Platforms
- Schoology (Engine v3)
- Veracross (Enginge v1)

#### Platforms In Development
- Flik lunch menu

#### Future Platforms
- Showbie
- Google Classroom

## How to use



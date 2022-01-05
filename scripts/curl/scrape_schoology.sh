# curling this server internally to test schoology scraper

curl http://localhost:8000/api/scrape -d "platform_code=sc" -d "user_id=1" -X POST -v
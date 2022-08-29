heroku login
heroku container:login

docker buildx build --platform linux/amd64 -t schoolverse-webscraper .
docker tag schoolverse-webscraper registry.heroku.com/schoolverse-webscraper/web
docker push registry.heroku.com/schoolverse-webscraper/web

heroku container:release web -a schoolverse-webscraper

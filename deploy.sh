#!/bin/bash
doctl registry login
docker buildx build --load --platform linux/amd64 -t registry.digitalocean.com/schoolverse/schoolverse-webscraper .
docker push registry.digitalocean.com/schoolverse/schoolverse-webscraper
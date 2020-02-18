docker build -t ipublica_scraper .
docker run --rm -ti -v $(pwd)/scraper:/src/scraper ipublica_scraper bash

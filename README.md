# check-my-ssl

[![Build Status](https://travis-ci.com/discopatrick/check-my-ssl.svg?branch=master)](https://travis-ci.com/discopatrick/check-my-ssl)

Unit tests: `docker-compose run --rm app python -m pytest /app/backend`

Functional tests: `behave` (from the host)

Cron job for live server daily SSL cert renewal: `0 4 * * * cd /home/deploy/check-my-ssl && /usr/local/bin/docker-compose -f docker-compose.yml -f env/production/compose.yml run --rm certbot renew --webroot --webroot-path=/data/letsencrypt --quiet && /usr/local/bin/docker-compose -f docker-compose.yml -f env/production/compose.yml kill -s HUP proxy`

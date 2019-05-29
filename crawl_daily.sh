#!/bin/bash

echo "crawl date: $(date)"
source /var/www/ACATblog/.venv/bin/activate
source /var/www/ACATblog/.env
flask crawl
deactivate

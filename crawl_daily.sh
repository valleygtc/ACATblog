#!/bin/bash
#With crontab.
#Crawl articles from blog sites.
echo "crawl date: $(date)"
source /var/www/ACATblog/venv/bin/activate
source /var/www/ACATblog/aliyun_env.sh
python3 /var/www/ACATblog/manage.py crawl
deactivate

echo "crawl date: $(date)" >>/var/www/ACATblog/crawl_daily.log
source /var/www/ACATblog/venv/bin/activate
source /var/www/ACATblog/aliyun_env.sh
python3 /var/www/ACATblog/manage.py crawl >>/var/www/ACATblog/crawl_daily.log

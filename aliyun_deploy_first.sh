#!bin/bash

#purpose:
#First deploy ACATblog on Aliyun(Ubuntu16.4)
##include init_db

#do:
#1.from aliyun_env.sh export env variables
#2.initialize database
#3.use apache2+mod_wsgi delpoy on aliyun

#usage:
#as root #:source aliyun_deploy_first.sh

#related file(path:/etc/mod_wsgi-express-80/):
#config :/etc/mod_wsgi-express-80/httpd.conf
#manipulate with /etc/mod_wsgi-express-80/apachectl [start|stop|restart]
#log :/etc/mod_wsgi-express-80/error_log
#...


source ./venv/bin/activate
source ./aliyun_env.sh

python3 ./manage.py init_db

mod_wsgi-express setup-server acatblog.wsgi \
--host=172.18.85.108 --port=80 \
--user=www-data --group=www-data \
--server-root=/etc/mod_wsgi-express-80
/etc/mod_wsgi-express-80/apachectl start
echo 'apache2 start on port 80'

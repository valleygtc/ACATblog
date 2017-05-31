#!bin/bash

#purpose:
#ACATblog Server Start on Aliyun(Ubuntu16.4)

#do:
#1.from aliyun_env.sh export env variables
#2.use apache2+mod_wsgi delpoy on aliyun

#usage:
#as root #:source aliyun_serverstart.sh

#related file(path:/etc/mod_wsgi-express-80/):
#config :/etc/mod_wsgi-express-80/httpd.conf
#manipulate with /etc/mod_wsgi-express-80/apachectl [start|stop|restart]
#log :/etc/mod_wsgi-express-80/error_log
#...


source ./venv/bin/activate
source ./aliyun_env.sh

mod_wsgi-express setup-server acatblog.wsgi \
--host=172.18.85.108 --port=80 \
--user=www-data --group=www-data \
--server-root=/etc/mod_wsgi-express-80

/etc/mod_wsgi-express-80/apachectl start
echo 'apache2 start on port 80'

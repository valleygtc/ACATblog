#!bin/bash

#purpose:
#To deploy ACATblog locally to try

#do:
#1.from dev_env.sh export env variables
#2.use apache2+mod_wsgi delpoy locally

#usage:
#as root #:source dev_deploy_local.sh

#related file(path:/etc/mod_wsgi-express-80/):
#config :/etc/mod_wsgi-express-80/httpd.conf
#manipulate with /etc/mod_wsgi-express-80/apachectl [start|stop|restart]
#log :/etc/mod_wsgi-express-80/error_log
#...


source ./venv/bin/activate
source ./dev_env.sh
mod_wsgi-express setup-server acatblog.wsgi \
--user=www-data --group=www-data \
--server-root=/etc/mod_wsgi-express-80
/etc/mod_wsgi-express-80/apachectl start

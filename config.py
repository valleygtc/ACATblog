import os


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'oh a secret key'

    @staticmethod
    def init_app(app):
        pass


class DevConfig(BaseConfig):
    DEBUG = True
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'db.sqlite')


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.environ['SECRET_KEY']
    ADMIN_USERNAME = os.environ['ADMIN_USERNAME']
    ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']

    @staticmethod
    def init_app(app):
        BaseConfig.init_app(app)
        # log to /var/www/ACATblog/crawler-verbose.log
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('/var/www/ACATblog/crawler-verbose.log',
                                           mode='a', maxBytes=2000)
        file_handler.setLevel(logging.INFO)
        app.logger.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {
    'development': DevConfig,
    'production': ProductionConfig,
}

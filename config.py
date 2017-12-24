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
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'db.sqlite')


class ProductConfig(BaseConfig):
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'db.sqlite')

    @staticmethod
    def init_app(app):
        BaseConfig.init_app(app)
        pass


class HerokuConfig(ProductConfig):
    @staticmethod
    def init_app(app):
        ProductConfig.init_app(app)
        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


class Aliyun(ProductConfig):
    @staticmethod
    def init_app(app):
        ProductConfig.init_app(app)
        # log to /var/www/ACATblog/crawler-verbose.log
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('/var/www/ACATblog/crawler-verbose.log',
                                           mode='a', maxBytes=2000)
        file_handler.setLevel(logging.INFO)
        app.logger.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {
    'develope': DevConfig,
    'production': ProductConfig,
    'heroku': HerokuConfig,
    'aliyun': Aliyun,

    'default': DevConfig,
}

#!usr/bin/python3.5
import os
from flask import current_app
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app import db
from app.models import Author, Article, Constant

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(db=db, Author=Author, Article=Article, Constant=Constant)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def init_db():
    current_app.logger.info('Database initilize begin...')
    db.drop_all()
    db.create_all()
    Author.init()
    Article.init()
    Constant.init()
    current_app.logger.info('initialize database done!')

@manager.command
def crawl():
    current_app.logger.info('Crawler begin.')
    Article.update()
    current_app.logger.info('Crawler done.')
    current_app.logger.info('Update table Constant begin.')
    Constant.update()
    current_app.logger.info('Update table Constant done.')


if __name__ == '__main__':
    manager.run()

#!usr/bin/python3.5
import os
from flask import current_app
from flask_migrate import Migrate
from app import create_app
from app import db
from app.models import Author, Article, Constant
import time

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


def make_shell_context():
    return dict(db=db, Author=Author, Article=Article, Constant=Constant)

app.shell_context_processor(make_shell_context)



@app.cli.command()
def init_db():
    current_app.logger.info('Database initilize begin...')
    db.drop_all()
    db.create_all()
    Author.init()
    Article.init()
    Constant.init()
    current_app.logger.info('initialize database done!')

@app.cli.command()
def crawl():
    current_app.logger.info(time.ctime() + ':Crawler begin.')
    Article.update()
    current_app.logger.info(time.ctime() + ':Crawler done.')
    current_app.logger.info(time.ctime() + ':Update table Constant begin.')
    Constant.update()
    current_app.logger.info(time.ctime() + ':Update table Constant done.')


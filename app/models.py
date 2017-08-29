from datetime import datetime
from . import db
from flask import current_app


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    blog_type = db.Column(db.String(20))
    blog_address = db.Column(db.String(80))
    last_get = db.Column(db.DateTime)
    avatar = db.Column(db.LargeBinary)
    flag = db.Column(db.Boolean)

    # 初始化authors
    @staticmethod
    def init():
        current_app.logger.info('Author initialize begin...')
        init_Author_from_file()
        current_app.logger.info('Author initialize done!')

    def __repr__(self):
        return '<Author %s>' % self.name


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    url = db.Column(db.String(80))
    pub_date = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('articles',order_by=pub_date.desc()))
    content_html = db.Column(db.Text)
    content_text = db.Column(db.Text)
    read_times = db.Column(db.Integer)

    # 初始化articles
    @staticmethod
    def init():
        current_app.logger.info('Article initilize begin...')
        authors = Author.query.all()
        for author in authors:
            from .crawler import get_articles
            get_articles(author, datetime(2017, 1, 1))
        current_app.logger.info('Article initilize done!')

    # 更新articles
    @staticmethod
    def update():
        current_app.logger.info('Begin the crawler to get articles...')
        authors = Author.query.all()
        for author in authors:
            from .crawler import get_articles
            get_articles(author, author.last_get)
        current_app.logger.info('Crawler done!')

    def __repr__(self):
        return '<Article %s>' % self.title


class Constant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_authors = db.Column(db.Integer)
    num_articles = db.Column(db.Integer)
    num_original = db.Column(db.Integer)
    num_unoriginal = db.Column(db.Integer)

    @staticmethod
    def init():
        articles = Article.query.all()
        num_authors = len(Author.query.all())
        num_articles = len(articles)
        count = 0
        for article in articles:
            if article.title[:3] == '[转]':
                count += 1
        num_unoriginal = count
        num_original = num_articles - count
        contant = Constant(num_authors=num_authors, num_articles=num_articles,
                           num_original=num_original, num_unoriginal=num_unoriginal)
        db.session.add(contant)
        db.session.commit()

    @staticmethod
    def update():
        constant = Constant.query.get(1)
        articles = Article.query.all()
        num_authors = len(Author.query.all())
        num_articles = len(articles)
        count = 0
        for article in articles:
            if article.title[:3] == '[转]':
                count += 1
        num_unoriginal = count
        num_original = num_articles - count
        constant.num_authors = num_authors
        constant.num_articles = num_articles
        constant.num_original = num_original
        constant.num_unoriginal = num_unoriginal
        db.session.add(constant)
        db.session.commit()


def init_Author_from_file():
    with open('init_data.txt', mode='r', encoding='utf-8') as file:
        for line in file:
            name, blog_address = line.strip().split(',')
            if 'csdn' in blog_address:
                blog_type = 'csdn'
                flag = True
            elif 'cnblogs' in blog_address:
                blog_type = 'cnblogs'
                flag = True
            elif 'sina' in blog_address:
                blog_type = 'sina'
                flag = True
            else:
                blog_type = 'others'
                flag = False
            author = Author(name=name, blog_type=blog_type, blog_address=blog_address, avatar=None,
                            flag=flag)
            db.session.add(author)
            from .crawler import get_avatar
            get_avatar(author)
    db.session.commit()

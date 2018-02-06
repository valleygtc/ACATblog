from datetime import datetime
import requests
from bs4 import BeautifulSoup
from . import db
from .models import Article
from flask import current_app

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}


def get_articles(author, from_date):
    if author.flag == False:
        current_app.logger.info('crawler:' + author.name + ' skipped(flag==False).')
        return None
    try:
        if author.blog_type == 'csdn':
            get_articles_csdn(author, from_date)
        if author.blog_type == 'cnblogs':
            get_articles_cnblogs(author, from_date)
        if author.blog_type == 'sina':
            get_articles_sina(author, from_date)
    except Exception as e:
        current_app.logger.warning('crawler:' + author.name + 'get_articles wrong!')
        current_app.logger.warning('verbose:' + str(e))
    else:
        current_app.logger.info('crawler:' + author.name + 'get_articles successfully!')


def get_avatar(author):
    try:
        if author.blog_type == 'csdn':
            get_avatar_csdn(author)
        else:
            default_avatar(author)
    except:
        current_app.logger.warning('crawler:' + author.name + 'get_avatar wrong!')
    else:
        current_app.logger.info('crawler:' + author.name + 'get_avatar successfully!')


def get_articles_csdn(author, from_date):
    rss_address = author.blog_address + '/rss/list'
    blog = requests.get(rss_address, headers=headers)
    rss = BeautifulSoup(blog.text, "html.parser")
    for item in rss.find_all('item'):
        # 注：beautiful会格式化传递给它的html，将所有的tag name变成小写的，所以pubdate要用小写的。
        pub_date = datetime.strptime(item.pubdate.string, '%Y/%m/%d %H:%M:%S')
        if pub_date > from_date:
            # 注：正常来说应该是item.description.string就行，但是不对，有点毛病，所以只好根据实际情况调整成下面那样
            content_html = item.description.contents[1].string
            # 优化：用re来实现提取阅读量
            content_soup = BeautifulSoup(content_html, "html.parser")
            read_times = int(content_soup.find_all('div')[-1].contents[0].strip().split('：')[1])
            article = Article(title=item.title.string,
                              url=item.link.string, pub_date=pub_date, author=author, content_html=content_html,
                              content_text=''.join(content_soup.get_text().split()), read_times=read_times)
            db.session.add(article)
        else:
            break
    author.last_get = datetime.now()
    db.session.add(author)
    db.session.commit()


def get_articles_cnblogs(author, from_date):
    rss_address = author.blog_address + '/rss'
    rss = requests.get(rss_address, headers=headers)
    soup = BeautifulSoup(rss.text, "html.parser")
    for entry in soup.find_all('entry'):
        pub_date = datetime.strptime(entry.published.string, '%Y-%m-%dT%H:%M:%SZ')
        if pub_date > from_date:
            article = Article(title=entry.title.string,
                              url=entry.id.string, pub_date=pub_date, author=author, content_html=entry.content.string,
                              content_text=''.join(entry.summary.string.split()), read_times=None)
            db.session.add(article)
        else:
            break
    author.last_get = datetime.now()
    db.session.add(author)
    db.session.commit()


def get_articles_sina(author, from_date):
    # blog_address:   http://blog.sina.com.cn/liy19980216
    # rss_address:    http://blog.sina.com.cn/rss/liy19980216.xml
    blog_host = author.blog_address.split('/')[-1]
    rss_address = 'http://blog.sina.com.cn/rss/' + blog_host + '.xml'
    rss = requests.get(rss_address, headers=headers)
    soup = BeautifulSoup(rss.text, "html.parser")
    for item in soup.find_all('item'):
        # <pubDate>Wed, 08 Mar 2017 21:30:39 +0800</pubDate>
        pub_date = datetime.strptime(item.pubdate.string, '%a, %d %b %Y %H:%M:%S +0800')
        if pub_date > from_date:
            article = Article(title=item.title.string,
                              url=item.link.string, pub_date=pub_date, author=author,
                              content_html=item.description.string,
                              content_text=''.join(
                                  BeautifulSoup(item.description.string, 'html.parser').get_text().split()),
                              read_times=None)
            db.session.add(article)
        else:
            break
    author.last_get = datetime.now()
    db.session.add(author)
    db.session.commit()


def get_avatar_csdn(author):
    home = requests.get(author.blog_address, headers=headers)
    soup = BeautifulSoup(home.text, "html.parser")
    pic_src = soup.select('img[src*="http://avatar.csdn.net"]')[0]['src']
    pic = requests.get(pic_src, headers=headers)
    author.avatar = pic.content
    db.session.add(author)
    db.session.commit()


# 默认使用ACAT协会的logo作为avatar
def default_avatar(author):
    with open('app/static/images/ACAT.jpg', 'rb') as f:
        author.avatar = f.read()
        db.session.add(author)
        db.session.commit()

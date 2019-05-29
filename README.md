# ACAT群博网站
## 简介
西安邮电大学计算机应用技术协会（ACAT）群博网站 web app 。定时爬取协会成员博客，汇总展示。

# 依赖：
python3.x

# 部署
```bash
$ git clone <repo>

# create virtual environment, install dependent package
$ cd ACATblog
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
 
$ touch .env # and config, .env文件内容参考见下

# run server
$ python run.py
```

.env文件参考内容：
```bash
export FLASK_APP=manage.py
export FLASK_ENV='development' # 'development' | 'production'
export SECRET_KEY='secret key'

export ADMIN_USERNAME='admin_username'
export ADMIN_PASSWORD='admin_password'
export DATABASE_URI='sqlite:///<db path>'

```

# 用到的技术
爬虫：requests, BeautifulSoup4

web app：Flask, Flask-SQLAlchemy

数据库：sqlite3

部署：waitress

# 开发人员名单
valleygtc: [github](https://github.com/valleygtc/)

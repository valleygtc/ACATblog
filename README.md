# ACAT群博网站
## 简介
此项目为西安邮电大学计算机应用技术协会的群博网站web app
其包含一个爬虫程序和一个HTTP web app

`用到的技术`

爬虫：requests, BeautifulSoup

web app：Flask, Flask-Migrate, Flask-SQLAlchemy

数据库：sqlite3

部署：Apache2-httpd-mod_wsgi

## 部署
依赖：`sudo install apache2,apache2-dev`、`sudo pip3 install mod_wsgi`

使用mod_wsgi-express来进行配置。


------------------

# ACATblog Web app
-------------
##  Description
This is a blog app used by ACAT(XUPT Association of Computer Application and Technology).

This consists of crawler and a normal web app.

The crawler can fetch blogs from  blog sites of our members.(CSDN,sina,cnblog)
It's just for study and communication.


## Deploy on Server
In Ubuntu 16.4

Dependencies:

sudo install apache2,apache2-dev

## License
No License.

You can use it for free.

## Author
valleygtc and Zhan Yongdong.

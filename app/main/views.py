from flask import render_template, session, Response, request
from . import main
from ..decorators import login_required
from ..models import Author, Article, Constant
from .. import db
# from .form import LoginForm, AddAuthorForm, ModifyAuthorForm, DeleteAuthorConfirm
from flask import current_app, flash, redirect, url_for
from datetime import datetime


@main.route('/')
def index():
    authors = Author.query.order_by(Author.grade.asc())

    def select_grade(authors, grade):
        group = []
        for author in authors:
            if author.grade == grade:
                group.append(author)
        return group

    # grade_groups为[[author,author...],[author,author...]...]的形式
    grade_groups = []
    grade_groups.append(select_grade(authors, 2014))
    grade_groups.append(select_grade(authors, 2015))
    grade_groups.append(select_grade(authors, 2016))
    grade_groups.append(select_grade(authors, 2017))

    page = request.args.get('page', 1, type=int)
    author_id = request.args.get('author_id', None, int)
    if author_id:
        pagination = Article.query.filter_by(author_id=author_id).order_by(Article.pub_date.desc()).paginate(page,
                                                                                                             per_page=10)
        pagination.author_id = author_id
    else:
        pagination = Article.query.order_by(Article.pub_date.desc()).paginate(page, per_page=10)
        pagination.author_id = None
    articles = pagination.items
    return render_template('index.html', grade_groups=grade_groups, articles=articles, pagination=pagination)


@main.route('/avatar/<int:author_id>')
def avatar(author_id):
    author = Author.query.filter_by(id=author_id).first()
    resp = Response(author.avatar, mimetype='image/jpg')
    return resp


@main.route('/admin', methods=['GET', 'POST'])
def admin_login():
    session['login'] = False
    if request.method == 'POST':
        if request.form['username'] == current_app.config['ADMIN_USERNAME'] and \
                        request.form['password'] == current_app.config['ADMIN_PASSWORD']:
            session['login'] = True
            flash('欢迎管理员大人登录')
            return redirect(url_for('main.manage'))
        else:
            flash('账号或密码错误')
    return render_template('admin_login.html')


@main.route('/logout')
@login_required
def admin_logout():
    session['login'] = False
    flash('Log out successfully!')
    return redirect(url_for('main.index'))


@main.route('/manage')
@login_required
def manage():
    authors = Author.query.all()
    return render_template('manage.html', authors=authors)


@main.route('/add-author', methods=['GET', 'POST'])
@login_required
def author_add():
    if request.method == 'POST':
        flag = True
        if request.form['blog_type'] == 'others':
            flag = False
        # 这里如果没有上传图片默认读取ACAT logo图片，如果图片移动了则会有问题，应该改一下。
        a = request.files['avatar'].read()
        if a:
            avatar = a
        else:
            avatar = open('app/static/images/ACAT.jpg', mode='rb').read()
        author = Author(name=request.form['name'], grade=int(request.form['grade']),
                        blog_type=request.form['blog_type'],
                        blog_address=request.form['blog_address'],
                        last_get=datetime.now(), avatar=avatar, flag=flag)
        db.session.add(author)
        db.session.commit()
        flash('成功添加Author：%s' % request.form['name'])
        return redirect(url_for('main.manage'))
    return render_template('author_add.html')


@main.route('/modify-author/<int:author_id>', methods=['GET', 'POST'])
@login_required
def author_modify(author_id):
    author = Author.query.filter_by(id=author_id).first()
    if request.method == 'POST':
        author.name = request.form['name']
        author.grade = request.form['grade']
        author.blog_type = request.form['blog_type']
        author.blog_address = request.form['blog_address']
        if request.form['flag'] == 'y' and not request.form['blog_type'] == 'others':
            author.flag = True
        else:
            author.flag = False
        a = request.files['avatar'].read()
        # 只有上传了avatar才会修改，未上传则不修改Author.avatar
        if a:
            author.avatar = a
        db.session.add(author)
        db.session.commit()
        flash('成功修改Author：%s的信息' % request.form['name'])
        return redirect(url_for('main.manage'))
    form = {}
    form['name'] = author.name
    form['grade'] = author.grade
    form['blog_type'] = author.blog_type
    form['blog_address'] = author.blog_address
    form['flag'] = author.flag
    return render_template('author_modify.html', form=form)


@main.route('/delete-author/<int:author_id>', methods=['GET', 'POST'])
@login_required
def author_delete(author_id):
    author = Author.query.filter_by(id=author_id).first()
    if request.method == 'POST':
        if request.form['confirm'] == 'y':
            db.session.delete(author)
            db.session.commit()
            flash('成功删除Author：%s' % author.name)
            return redirect(url_for('main.manage'))
    return render_template('author_delete.html', author=author)


# 官网上的近期活动：公众号文章
@main.route('/redirect-to-sogou')
def tosogou():
    from wechatsogou import WechatSogouAPI
    wx_api = WechatSogouAPI()
    profile_url = wx_api.get_gzh_info('xuptacat')['profile_url']
    return redirect(profile_url)

from flask import render_template, session, Response, request
from . import main
from ..decorators import login_required
from ..models import Author, Article, Constant
from .. import db
from .form import LoginForm, AddAuthorForm, ModifyAuthorForm, DeleteAuthorConfirm
from flask import current_app, flash, redirect, url_for
from datetime import datetime


@main.route('/')
def index():
    authors = Author.query.all()
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.pub_date.desc()).paginate(page, per_page=10)
    articles = pagination.items
    return render_template('index.html', authors=authors, articles=articles, pagination=pagination)


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
        if 'avatar' not in request.files:
            # 这里如果没有上传图片默认读取ACAT logo图片，如果图片移动了则会有问题，应该改一下。
            avatar = open('app/static/images/ACAT.jpg', mode='rb').read()
        else:
            avatar = request.files['avatar'].read()
        author = Author(name=request.form['name'], blog_type=request.form['blog_type'],
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
    form = ModifyAuthorForm()
    author = Author.query.filter_by(id=author_id).first()
    if form.validate_on_submit():
        author.name = form.name.data
        author.blog_type = form.blog_type.data
        author.blog_address = form.blog_address.data
        author.flag = form.flag.data
        if form.blog_type.data == 'others':
            author.flag = False
        if form.avatar.data:
            author.avatar = form.avatar.data.read()
        db.session.add(author)
        db.session.commit()
        flash('Modify %s Successfully' % form.name.data)
        return redirect(url_for('main.manage'))
    else:
        form.name.data = author.name
        form.blog_type.data = author.blog_type
        form.blog_address.data = author.blog_address
        form.flag.data = author.flag
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


# 使用Flask-Form的版本
# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     session['login'] = False
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.username.data == current_app.config['ADMIN_USERNAME'] and \
#                         form.password.data == current_app.config['ADMIN_PASSWORD']:
#             session['login'] = True
#             flash('Welcome Admin')
#         else:
#             flash('Username or Password wrong!')
#     return redirect(url_for('main.index'))

# @main.route('/add-author', methods=['GET', 'POST'])
# @login_required
# def author_add():
#     form = AddAuthorForm()
#     if form.validate_on_submit():
#         flag = True
#         if form.blog_type == 'others':
#             flag = False
#         author = Author(name=form.name.data, blog_type=form.blog_type.data, blog_address=form.blog_address.data,
#                         last_get=datetime.now(), avatar=form.avatar.data.read(), flag=flag)
#         db.session.add(author)
#         db.session.commit()
#         flash('Add %s Successfully!' % form.name.data)
#         return redirect(url_for('main.manage'))
#     return render_template('author_add.html', form=form)

# @main.route('/modify-author/<int:author_id>', methods=['GET', 'POST'])
# @login_required
# def author_modify(author_id):
#     form = ModifyAuthorForm()
#     author = Author.query.filter_by(id=author_id).first()
#     if form.validate_on_submit():
#         author.name = form.name.data
#         author.blog_type = form.blog_type.data
#         author.blog_address = form.blog_address.data
#         author.flag = form.flag.data
#         if form.blog_type.data == 'others':
#             author.flag = False
#         if form.avatar.data:
#             author.avatar = form.avatar.data.read()
#         db.session.add(author)
#         db.session.commit()
#         flash('Modify %s Successfully' % form.name.data)
#         return redirect(url_for('main.manage'))
#     else:
#         form.name.data = author.name
#         form.blog_type.data = author.blog_type
#         form.blog_address.data = author.blog_address
#         form.flag.data = author.flag
#     return render_template('author_modify.html', form=form)


# @main.route('/delete-author/<int:author_id>', methods=['GET', 'POST'])
# @login_required
# def author_delete(author_id):
#     author = Author.query.filter_by(id=author_id).first()
#     form = DeleteAuthorConfirm()
#     if form.validate_on_submit():
#         if form.confirm.data:
#             db.session.delete(author)
#             db.session.commit()
#             flash('Delete %s successfully.' % author.name)
#             return redirect(url_for('main.manage'))
#     return render_template('author_delete.html', form=form, author=author)


# 官网上的近期活动：公众号文章
@main.route('/redirect-to-sogou')
def tosogou():
    from wechatsogou import WechatSogouAPI
    wx_api = WechatSogouAPI()
    profile_url = wx_api.get_gzh_info('xuptcal')['profile_url']
    return redirect(profile_url)

# 线上那个原版需要用的
# @main.app_template_filter('group')
# def group(authors, number):
#     groups = []
#     for index, author in enumerate(authors, 1):
#         if index % number == 1:
#             groups.append([author])
#         else:
#             groups[-1].append(author)
#     return groups

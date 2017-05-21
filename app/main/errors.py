from flask import request, render_template
from . import main
from .form import LoginForm


@main.app_errorhandler(403)
def forbidden(e):
    form = LoginForm()
    return render_template('403.html', login_form=form), 403


@main.app_errorhandler(404)
def page_not_found(e):
    form = LoginForm()
    return render_template('404.html', login_form=form), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    form = LoginForm()
    return render_template('500.html', login_form=form), 500

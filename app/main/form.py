from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class AddAuthorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    blog_type = SelectField('Blog Type', validators=[DataRequired()],
                            choices=[('csdn', 'csdn'), ('cnblogs', 'cnblogs'), ('sina', 'sina'), ('others', 'others')])
    blog_address = StringField('Blog Address', validators=[DataRequired()])
    flag = BooleanField('Flag True')
    avatar=FileField('Avatar',validators=[FileRequired('Avatar required!')])
    submit = SubmitField('Add')


class ModifyAuthorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    blog_type = SelectField('Blog Type', validators=[DataRequired()],
                            choices=[('csdn', 'csdn'), ('cnblogs', 'cnblogs'), ('sina', 'sina'), ('others', 'others')])
    blog_address = StringField('Blog Address', validators=[DataRequired()])
    flag = BooleanField('Flag True')
    avatar = FileField('Avatar')
    submit = SubmitField('Submit')


class DeleteAuthorConfirm(FlaskForm):
    confirm = BooleanField('Confirm', validators=[DataRequired()])
    submit = SubmitField('Submit')

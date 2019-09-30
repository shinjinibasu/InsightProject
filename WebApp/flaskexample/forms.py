from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('User ID', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Get recommendation!')

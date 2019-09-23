from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    username=StringField('Username',validators=[DataRequired('名字不能为空')])
    password=PasswordField('Password',validators=[DataRequired(),Length(8,128)])
    remember=BooleanField('Remember me')
    submit=SubmitField('Login')
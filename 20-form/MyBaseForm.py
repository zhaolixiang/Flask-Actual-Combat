from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SubmitField, IntegerField, FileField, MultipleFileField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length


class MyBaseForm(FlaskForm):
    class Meta:
        locales=['zh']


class HelloForm(MyBaseForm):
    name=StringField('Name',validators=[DataRequired()])
    submit=SubmitField()

class FortyTwoForm(MyBaseForm):
    answer=IntegerField('The Number')
    submit=SubmitField()

    def validate_answer(form,field):
        if field.data!=42:
            raise ValidationError('Must be 42.')


def is_42(form,field):
    if field.data!=42:
        raise ValidationError('Must be 42')

class FortyTwoForm2(MyBaseForm):
    answer=IntegerField('The Number',validators=[is_42])
    submit=SubmitField()

def is_42(message=None):
    if message is None:
        message='Must be 42'

    def _is_42(form,field):
        raise ValidationError(message)
    return _is_42

class FortyTwoForm3(MyBaseForm):
    answer=IntegerField('The Number',validators=[is_42('自定义错误信息')])
    submit=SubmitField()


class UploadForm(MyBaseForm):
    photo=FileField('Upload Image',
                    validators=[FileRequired(),FileAllowed(['jpg','jpeg','png','gif'])])
    submit=SubmitField()


class MultiUploadForm(MyBaseForm):
    photo=MultipleFileField('Upload Image',
                    validators=[DataRequired(),FileAllowed(['jpg','jpeg','png','gif'])])
    submit=SubmitField()

class RichTextForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired(),Length(1,50)])
    body=CKEditorField('Body',validators=[DataRequired])
    submit=SubmitField('Publish')

class NewPostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired(),Length(1,50)])
    body=TextAreaField('Body',validators=[DataRequired()])
    save=SubmitField('Save') #保存按钮
    publish=SubmitField('Publish') # 发布按钮

class SigninForm(FlaskForm):
    username=StringField('Title',validators=[DataRequired(),Length(1,50)])
    submit1=SubmitField('Sign in')

class RegisterForm(FlaskForm):
    username = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    submit2=SubmitField('Register')
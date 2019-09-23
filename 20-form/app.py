import uuid

from flask import Flask, render_template, request, flash, redirect, url_for, session, send_from_directory
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError

from .forms import LoginForm
import os


app=Flask(__name__)
app.secret_key='qqqwwweeeerrrr'
app.config['WTF_I18N_ENABLED']=False
app.config['MAX_CONTENT_LENGTH']=3*1024*1024
app.config['UPLOAD_PATH']=os.path.join(app.root_path,'uploads')
app.config['ALLOWED_EXTENSIONS']=['png','jpg','jpeg','gif']
app.config['CKEDITOR_SERVE_LOCAL']=True

@app.route('/html')
def html():
    return render_template('html.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/basic',methods=['GET','POST'])
def basic():
    form=LoginForm()
    # if request.method=='POST' and form.validate():
    if form.validate_on_submit():
        # 处理POST请求
        username=form.username.data
        flash('Welcome home,%s'%username)
        print('看这里')
        return redirect(url_for('index'))
    # 处理GET请求
    return render_template('basic.html',form=form)

@app.route('/bootstrap')
def bootstrap():
    form=LoginForm()
    return render_template('bootstrap.html',form=form)

from .MyBaseForm import UploadForm,MultiUploadForm,NewPostForm,SigninForm,RegisterForm

@app.route('/upload',methods=['GET','POST'])
def upload():
    form=UploadForm()
    if form.validate_on_submit():
        f=form.photo.data
        filename=random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'],filename))
        flash('Upload success')
        session['filenames']=[filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html',form=form)


def random_filename(filename):
    ext=os.path.split(filename)[1]
    new_filename=uuid.uuid4().hex+ext
    return new_filename

@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'],filename)

@app.route('/multi-upload',methods=['GET','POST'])
def multi_upload():
    form=MultiUploadForm()
    if request.method=='POST':
        filenames=[]
        # 验证CSRF令牌
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF token error')
            return redirect(url_for('multi_upload'))
        # 检查文件是否存在
        if 'photo' not in request.files:
            flash('This field')
            return redirect(url_for('multi_upload'))
        for f in request.files.getlist('phone'):
            # 检查文件类型
            if f and allowed_file(f.filename):
                filename=random_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_PATH'],filename))
                filenames.append(filename)
            else:
                flash('Invalid file type.')
                return redirect(url_for('multi_upload'))

        flash('Upload success')
        session['filenames']=filenames
        return redirect(url_for('show_images'))
    return render_template('multi-upload.html',form=form)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def two_submits():
    form=NewPostForm()
    if form.validate_on_submit():
        if form.save.data:
            flash('点击了保存按钮')
        elif form.publish.data:
            flash('点击了Publish按钮')
        return redirect(url_for('index'))
    return render_template('2submit.html',form=form)

@app.route('/multi-form',methods=['GET','POST'])
def multi_form():
    signin_form=SigninForm()
    register_form=RegisterForm()
    if signin_form.submit1.data and signin_form.validate_on_submit():
        flash('signin表单被点击了')
    elif register_form.submit2.data and register_form.validate_on_submit():
        flash('register表单被点击了')
    return render_template('2form.html',signin_form=signin_form,register_form=register_form)

from flask_ckeditor import CKEditor
if __name__ == '__main__':
    app.run()
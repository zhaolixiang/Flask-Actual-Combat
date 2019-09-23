import click
from flask import Flask, flash, render_template, redirect, url_for, abort
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

from flask_wtf import FlaskForm
from sqlalchemy.orm import backref
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'xxx'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate=Migrate(app,db)
mail=Mail(app)


@app.route('/')
def index():
    notes = Note.query.all()
    delete_form=DeleteNoteForm()
    return render_template('index.html', notes=notes,form=delete_form )


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)

    def __repr__(self):
        return '<Note %r>' % self.body


@app.cli.command()
@click.option('--drop',is_flag=True,help='Create after drop')
def initdb(drop):
    "Initialize the database"
    if drop:
        click.confirm('改操作将会删除你原来的数据库，是否要删除',abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('初始化数据库完成')


class NewNoteForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Save')


@app.route('/new_note', methods=['get', 'post'])
def new_note():
    form = NewNoteForm()
    if form.validate_on_submit():
        body = form.body.data
        note = Note(body=body)
        db.session.add(note)
        db.session.commit()
        flash('保存成功了')
        return redirect(url_for('index'))
    return render_template('new_note.html', form=form)


# class EditNoteForm(FlaskForm):
#     body=TextAreaField('body',validators=[DataRequired])
#     submit=SubmitField('Update')

class EditNoteForm(NewNoteForm):
    submit = SubmitField('Update')


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    form = EditNoteForm()
    note = Note.query.get(note_id)
    if form.validate_on_submit():
        note.body = form.body.data
        db.session.commit()
        flash('更细成功')
        return redirect(url_for('index'))
    form.body.data = note.body
    return render_template('edit_note.html', form=form)

class DeleteNoteForm(FlaskForm):
    submit=SubmitField('Delete')

@app.route('/delete/<int:note_id>',methods=['get','post'])
def delete_note(note_id):
    form=DeleteNoteForm()
    if form.validate_on_submit():
        # 获取对应记录
        note=Note.query.get(note_id)
        # 删除记录
        db.session.delete(note)
        # 提交修改
        db.session.commit()
        flash('删除成功')
    else:
        abort(400)
    return redirect(url_for('index'))

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Note=Note)


class Author(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),unique=True)
    phone=db.Column(db.String(20))
    articles=db.relationship('Atricle')

class Article(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(70),index=True)
    body=db.Column(db.Text)
    author_id=db.Column(db.Integer,db.ForeignKey('author.id'))

class Writer(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),unique=True)
    books=db.relationship('Book',back_populates='writer')

class Book(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),index=True)
    writer_id=db.Column(db.Integer,db.ForeignKey('writer.id'))
    writer=db.relationship('Writer',back_populates='books')

class Singer(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),unique=True)
    songs=db.relationship('Song',backref=backref('singer',uselist=False))
    # songs=db.relationship('Song',backref='singer')


class Song(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),index=True)
    singer_id=db.Column(db.Integer,db.ForeignKey('singer.id'))

class Citizen(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),unique=True)
    city_id=db.Column(db.Integer,db.ForeignKey('city.id'))
    city=db.relationship('City')

class City(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),unique=True)

class Country(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True)
    capital=db.relationship('Capital',uselist=False)

class Capital(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),unique=True)
    country_id=db.Column(db.Integer,db.ForeignKey('country.id'))
    country=db.relationship('Country')

association_table=db.Table('association',
                           db.Column('student_id',db.Integer,db.ForeignKey('student.id')),
                           db.Column('teacher_id',db.Integer,db.ForeignKey('teacher.id'))
                           )
class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),unique=True)
    grade=db.Column(db.String(20))
    teachers=db.relationship('Teacher',secondary=association_table,back_populates='students')

class Teacher(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(70),unique=True)
    office=db.Column(db.String(20))
    students=db.relationship('Student',secondary=association_table,back_populates='teachers')


if __name__ == '__main__':
    app.run()

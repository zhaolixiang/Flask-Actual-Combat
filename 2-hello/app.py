import click
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello Flask!</h1>'


@app.route('/greet',defaults={'name':'mark'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello,%s!</h1>'%name

@app.cli.command()
def hello():
    click.echo('Hello,Mark')


if __name__ == '__main__':
    app.run()

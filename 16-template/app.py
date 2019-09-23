from flask import Flask, render_template, flash, redirect, url_for
from markupsafe import Markup

app = Flask(__name__)
app.secret_key='secret string'

user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.',
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


@app.route('/')
def index():
    return render_template('index.html')


@app.context_processor
def inject_foo():
    print('app.context_processor执行了')
    foo = 'I am foo.'
    return dict(foo=foo)  # 等同于 return {'foo':foo}


@app.template_global('bar')
def bar():
    print('全局函数bar')
    return 'I am bar.'


@app.template_filter('musical')
def musical(s):
    return s + Markup('&#9835;')


@app.template_test('baz')
def baz(n):
    return n == 'baz'


def mark():
    return 'I am mark.'


face = 'I am Face'

# app.jinja_env.globals['mark'] = mark
# app.jinja_env.globals['face'] = face


def smiling(s):
    return s + ':)'


# app.jinja_env.filters['smiling'] = smiling
# app.jinja_env.filters['musical'] = musical


def love(n):
    return n == 'love'


# app.jinja_env.tests['love'] = love
# app.jinja_env.tests['baz'] = baz



@app.route('/flash')
def just_flash():
    flash('I am flask,who is looking for me')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'),404

if __name__ == '__main__':
    app.run()

import os

from flask import Flask, request, make_response, url_for, redirect, session, g

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default')


@app.route('/')
@app.route('/hello', methods=['get', 'post'])
def hello():
    name = request.args.get('name', None)
    if name is None:
        name = request.cookies.get('name', 'face')
    response = '<h1>Hello,%s!</h1>' % name
    if 'logged_in' in session:
        response += '已经登录了'
    else:
        response += '还没有登录呦'
    return response


@app.route('/goback/<int:year>')
def gp_back(year):
    return 'Welcome to %d' % (2019 - year)


@app.route('/color/<any(blue,white,red):color>')
def three_colors(color):
    return color


@app.route('/baidu')
def baidu():
    return '', 302, {'Location': 'http://www.baidu.com'}


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


@app.route('/login')
def login():
    # 写入 session
    session['logged_in'] = True
    return redirect(url_for('hello'))


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


@app.before_request
def get_name():
    g.name = request.args.get('name')
    print('before_request获取到的那么', g.name)


@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do something</a>' % url_for('do_something')


@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something</a>' % url_for('do_something2')


@app.route('/foo2')
def foo2():
    return '<h1>Foo2 page</h1><a href="%s">Do something</a>' \
           % url_for('do_something', next=request.full_path)


@app.route('/do_something')
def do_something():
    return redirect(request.referrer or url_for('hello'))


@app.route('/do_something2')
def do_something2():
    return redirect(request.args.get('next', url_for('hello')))


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if target:
            return redirect(target)
    return redirect(url_for(default, **kwargs))


@app.route('/do_something3')
def do_something3():
    return redirect_back()


from urllib.parse import urlparse, urljoin


def is_safe_url(target):
    # host_url:http://www.baidu.com/
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back2(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


from jinja2.utils import generate_lorem_ipsum


@app.route('/post')
def show_post():
    # 生成两端随机文本
    post_bodt = generate_lorem_ipsum(n=2)
    return """
    <h1>A very long post</h1>
    <div class="body">%s</div>
    <button id="load">Load More</button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
        $(function(){
            $('#load').click(function(){
                $.ajax({
                    url:'/more',//目标URL
                    type:'get', //请求方法
                    success:function(data){ //返回2XX响应后触发的回调函数
                        $('.body').append(data); //将返回的响应插入到页面中
                    }
                })
            })
        })
    </script>
    """ % post_bodt


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)


if __name__ == '__main__':
    app.run()

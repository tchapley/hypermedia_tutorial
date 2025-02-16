import datetime
from flask import (
    Flask, redirect, render_template, request, flash
)
from posts_model import Post

Post.load_db()

app = Flask(__name__)

app.secret_key = b'hypermedia rocks'

@app.route('/')
def index():
    return redirect('/posts')

@app.route('/posts')
def posts():
    search = request.args.get('q')
    if search is not None:
        posts_set = Post.search(search)
    else:
        posts_set = Post.all()

    return render_template('index.html', posts=posts_set)

@app.route('/posts/new', methods=['GET'])
def posts_new_get():
    return render_template('new.html', post=Post())

@app.route('/posts/new', methods=['POST'])
def posts_new():
    p = Post(
        None,
        request.form['title'],
        request.form['body'],
        str(datetime.date.today())
    )
    if p.save():
        flash("Created New Post!")
        return redirect('/posts')
    else:
        return render_template('new.html', post=p)

@app.route('/posts/<post_id>')
def posts_view(post_id=0):
    post = Post.find(post_id)
    return render_template('show.html', post=post)

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
    page = int(request.args.get('page', 1))
    if search is not None:
        posts_set = Post.search(search)
        if request.headers.get('HX-Trigger') == 'search':
            return render_template('rows.html', posts=posts_set)
    else:
        posts_set = Post.all(page)

    return render_template('index.html', posts=posts_set, page=page)

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


@app.route('/posts/<post_id>/edit', methods=['GET'])
def posts_edit_get(post_id=0):
    post = Post.find(post_id)
    return render_template('edit.html', post=post)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def posts_edit(post_id=0):
    p = Post.find(post_id)
    p.update(
        request.form['title'],
        request.form['body']
    )
    if p.save():
        flash("Updated Contact!")
        return redirect('/posts/' + str(post_id))
    else:
        return render_template('edit.html', post=p)

@app.route('/posts/<post_id>', methods=['DELETE'])
def posts_delete(post_id=0):
    post = Post.find(post_id)
    post.delete()
    flash("Deleted Contact!")
    return redirect('/posts', 303)

@app.route('/posts/<post_id>/title', methods=['GET'])
def posts_title_get(post_id=0):
    p = Post.find(post_id)
    p.title = request.args.get('title')
    p.validate()
    return p.errors.get('title') or ""

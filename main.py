from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:lc101@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

tasks = []

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(10000))

    def __init__(self, title, body):
        self.name = title
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():

    #if request.method == 'POST':
        #blog_title = request.form['title']
        #blog_post = request.form['body']
        #new_post = Blog(blog_title, blog_post)
        #db.session.add(new_post)
        #db.session.commit()
    

    blogs = Blog.query.all()

    return render_template('blog.html', title_main="Hello Blog",
        blogs=blogs) #, completed_tasks=completed_tasks)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    
    subtitle = 'Add  a new blog post.'
    title_main = 'Hello Blog'
    title_error = ''
    post_error = ''
    title = ''
    body = ''
    
    if request.method == 'GET':
        return render_template('newpost.html', title_main="Hello Blog", subtitle="Add a new blog post.")

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_post = request.form['body']
        new_post = Blog(blog_title, blog_post)
        #db.session.add(new_post)
        #db.session.commit()

    #Title verification
    if len(blog_title) == 0:
        title_error = 'Please enter a title.'

    if len(blog_post) == 0:
        post_error = 'Please enter a post.'

    if not title_error and not post_error:
        db.session.add(new_post)
        db.session.commit()

        return redirect('/')

    else:
        return render_template('newpost.html', title_main=title_main, subtitle=subtitle, title=blog_title, body=blog_post, title_error=title_error, post_error=post_error)


if __name__ == '__main__':
    app.run()
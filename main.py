from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:lc101@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(10000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, blog_user_id):
        self.title = title
        self.body = body
        self.blog_user_id = blog_user_id

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='user')


    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        #validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    
    blogs = Blog.query.all()

    return render_template('blog.html', title_main="Hello Blog", blogs=blogs) 

@app.route('/blog', methods=['POST', 'GET'])
def weblog():
    id = request.args.get('id')
    
    if id == None:
        blogs = Blog.query.all()

        return render_template('blog.html', title_main="Hello Blog", blogs=blogs) 

    else:
        blog = Blog.query.get(id)
        return render_template('blog-entry.html', title_main="Hello Blog", blog=blog)
    

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    
    subtitle = 'Add  a new blog post.'
    title_main = 'Hello Blog'
    title_error = ''
    post_error = ''
    title = ''
    body = ''

    blog_user_id = request.args.get('owner_id')
    
    if request.method == 'GET':
        return render_template('newpost.html', title_main="Hello Blog", subtitle="Add a new blog post.")

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_post = request.form['body']
        new_post = Blog(blog_title, blog_post, blog_user_id)

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

@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect('/blog')

    
#@app.route('/logout', methods=['POST'])
#def logout():



if __name__ == '__main__':
    app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()
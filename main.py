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
    body = db.Column(db.String(5000))

    def __init__(self, title, body):
        self.name = name
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['title']
        new_post = Task(task_name)
        db.session.add(new_task)
        db.session.commit()
    tasks = Task.query.filter_by(completed=False).all()

    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('todos.html', title="Get It Done!", 
        tasks=tasks, completed_tasks=completed_tasks)

@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()
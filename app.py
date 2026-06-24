from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r >'% self.id
    
@app.route("/")
def loading():
    return render_template("loading.html")

@app.route ("/home", methods=['POST', 'GET'])
def index():
    # Logic for adding a task thats why we use POST
    if request.method == "POST":
        task_content =request.form['content'] # Create a new task 
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task) # Adding this to ower database session
            db.session.commit()
            return redirect("/") #Back to home Page
        
        except: # Just in case it fails to added a task
            return "There was an issue adding your Task"
            
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # This is going to look at all of the database contents in the date/order they were created 
        return render_template("index.html", tasks = tasks)

@app.route("/delete/<int:id>")

def delete(id):
    task_to_delete = Todo.query.get_or_404(id) # Var for task we want to delete

    try:
        db.session.delete(task_to_delete) # Deletes froms database
        db.session.commit()
        return redirect("/") #Back to home Page
    except:
        return "There was a problem deleting that task"
    

@app.route("/update/<int:id>", methods=["GET", "POST"])

def update(id):

    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form["content"] 

        try: # Use only commit cause we are update not adding or deleting
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue Updating your Task"
    else:
        return render_template("update.html",task=task)

if __name__ == "__main__":
    app.run(debug=True)
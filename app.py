from flask import Flask, render_template, redirect, url_for, request    #importing flask module
from flask_sqlalchemy import SQLAlchemy
#from flask_scss import Scss
from datetime import datetime   #importing datetime module

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db=SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(20), unique=True, nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    def __repr__(self):
        return f"Task{self.id}"



@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = MyTask(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()

        return render_template("main.html", tasks=tasks)
    
    return render_template("main.html")


@app.route("/delete/<int:id>")
def delete(id:int):
    task_to_delete = MyTask.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
    

@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id:int):
    task = MyTask.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template("about.html", task=task)
    
    return render_template("main.html")




if __name__=='__main__':
    with app.app_context():
        db.create_all()
         
    app.run(debug=True)
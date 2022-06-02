from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        Todo = todo(title=title, desc=desc)
        db.session.add(Todo)
        db.session.commit()
    
    alltodo = todo.query.all()
    return render_template("index.html", alltodo=alltodo)

# @app.route("/show")
# def products():
#     alltodo = todo.query.all()
#     print(alltodo)
#     return "This is a Product Page"

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        Todo = todo.query.filter_by(sno=sno).first()
        Todo.title = title
        Todo.desc = desc
        db.session.add(Todo)
        db.session.commit()
        return redirect("/")

    Todo = todo.query.filter_by(sno=sno).first()
    return render_template("update.html", alltodo=Todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    alltodo = todo.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect("/")

    return redirect("/")
if __name__=="__main__":
    app.run(debug=True)
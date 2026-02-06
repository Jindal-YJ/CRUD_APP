from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()


class Employee(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), nullable=False)


# ================= HOME (ADD + SORT) =================
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        employee = Employee(name=name, email=email)
        db.session.add(employee)
        db.session.commit()
        return redirect("/")

    # SORT LOGIC
    sort = request.args.get("sort")

    if sort == "asc":
        allemployee = Employee.query.order_by(Employee.sno.asc()).all()
    elif sort == "desc":
        allemployee = Employee.query.order_by(Employee.sno.desc()).all()
    else:
        allemployee = Employee.query.all()

    return render_template("index.html", allemployee=allemployee)


# ================= DELETE MULTIPLE =================
@app.route("/delete-multiple", methods=["POST"])
def delete_multiple():
    ids = request.form.getlist("selected_ids")

    if ids:
        Employee.query.filter(Employee.sno.in_(ids)).delete(synchronize_session=False)
        db.session.commit()

    return redirect("/")


@app.route("/delete/<int:sno>")
def delete(sno):
    employee = Employee.query.filter_by(sno=sno).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect("/")


# ================= UPDATE =================
@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    employee = Employee.query.filter_by(sno=sno).first()

    if request.method == 'POST':
        employee.name = request.form['name']
        employee.email = request.form['email']
        db.session.commit()
        return redirect("/")

    return render_template("update.html", employee=employee)


# ================= EXTRA ROUTES (UNCHANGED) =================
@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/dashboard")
def dash():
    items = ["apple", "banana", "cherry", "date"]
    return render_template("dashboard.html", data=items)


@app.route("/contact")
def f2():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)

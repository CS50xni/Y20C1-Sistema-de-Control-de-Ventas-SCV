from cs50 import SQL
from flask import Flask, render_template, session, request, flash, redirect
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required



db = SQL("sqlite:///scv.db")

app = Flask(__name__)

db = SQL("sqlite:///scv.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
@login_required
def acceder():
    row = db.execute("SELECT * FROM clientes WHERE usuario = :usuario",
                    username = request.form.get("usuario"))

@app.route("/register", methods=["POST", "GET"])
@login_required
def registro():
    if request.method == "POST":
        if not request.form.get("usuario"):
            flash("Ingrese un usuario")
        if not request.form.get("password"):
            flash("Ingrese una contraseña")
        password = generate_password_hash(request.form.get("password"))
        new_id = db.execute("INSERT INTO clientes (usuario, contaseña) VALUES (:usuario, :password)",
                            usuario=request.form.get("usuario"),password=password)
        session["usuario"] = new_id
        flash("Usted esta registrado")
        return redirect ("index.html")
    else:
        return render_template("PageRegister.html")
from flask import Flask, render_template, flash, redirect, request, session, url_for, jsonify
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from flask_session import Session
from tempfile import mkdtemp


app = Flask(__name__)
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configuramos la sesion
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Conectamos la base de datos
db = SQL("sqlite:///scv.db")


def cargarCarrito():
    ver = db.execute("Select * from carrito where id_cliente= :id_cliente and estado = 0", id_cliente = session["user_id"] )
    if(len(ver) == 0):
        return db.execute("INSERT INTO carrito(id_cliente) VALUES (:idcliente)", idcliente = session["user_id"])
    else:
        return ver[0]["id_carrito"]


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/index")
# Nos auxiliamos de funciones del pset7 para proteger el contenido de la pagina
# si el usuario no se ha registrado
@login_required
def index():
    return render_template("index.html")

@app.route("/inicio")
@login_required
def inicio():
    return render_template("inicio.html")

@app.route("/history")
@login_required
def history():
    return render_template("history.html")

@app.route("/home")
def cerrar():
    session.clear()
    return redirect(url_for("home"))

@app.route("/reservas")
def reservas():
    id_carrito = cargarCarrito()
    detalles = db.execute("SELECT * FROM detalle_carrito WHERE id_carrito = :idcar", idcar = id_carrito)
    total = 0.0
    for detalle in detalles:
        total += detalle["precio"] * detalle["cantidad"]
    return render_template("reservas.html", detalles = detalles, total = total)

@app.route("/lapices")
def lapices():

    id_carrito = cargarCarrito()
    return render_template("lapices.html")

@app.route("/marcadores")
def marcadores():
    id_carrito = cargarCarrito()
    return render_template("marcadores.html")

@app.route("/audifonos")
def audifonos():
    id_carrito = cargarCarrito()
    return render_template("audifonos.html")

@app.route("/memorias")
def memorias():
    id_carrito = cargarCarrito()
    return render_template("memorias.html")

@app.route("/cuadernos")
def cuadernos():
    id_carrito = cargarCarrito()
    return render_template("cuadernos.html")

@app.route("/login", methods=["GET", "POST"])
def acceder():
    session.clear()
    if request.method == "POST":
        # Verificamos la entrada que no sea vacia
        if not request.form.get("user"):
            flash("Ingrese su usuario.")
            return render_template("acceder.html")
        elif not request.form.get("password"):
            flash("Ingrese su contraseña")
            return render_template("acceder.html")
            #Buscamos el usuario en la base de datos
        rows = db.execute("SELECT * FROM clientes WHERE user = :user", user = request.form.get("user"))
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("Datos Incorrectos")
            return render_template("acceder.html")
        # Si los datos son correctos inicio de sesion
        session["user_id"] = rows[0]["id"]
        return redirect(url_for("history"))
    else:
        return render_template("acceder.html")

@app.route("/register", methods=["POST", "GET"])
def register():

    session.clear()

    if request.method == "POST":
        if not request.form.get("names"):
            flash("Ingrese su nombre.")
            return render_template("register.html")
        elif not request.form.get("phone"):
            flash("Ingrese una forma de contactarle")
            return render_template("register.html")
        elif not request.form.get("user"):
            flash("Ingrese un nombre de ususario")
            return render_template("register.html")
        elif not request.form.get("password"):
            flash("Ingrese una contraseña")
            return render_template("register.html")
        password = generate_password_hash(request.form.get("password"))
        new_id = db.execute("INSERT INTO clientes (user, password, names, phone) VALUES (:user, :password, :names, :phone)",
                            user=request.form.get("user"),
                            names=request.form.get("names"),
                            phone=request.form.get("phone"),
                            password=password)
        session["user_id"] = new_id
        return redirect(url_for("history"))
    else:
        return render_template("register.html")


@app.route("/agregarDetalle")
def cargarDetalle():
    id_carrito = cargarCarrito()
    nombre = request.args.get("nombre")
    precio = request.args.get("precio")
    cantidad = request.args.get("cantidad")
    categoria = request.args.get("categoria")

    res = db.execute("INSERT INTO detalle_carrito (id_carrito, nombre_prod, cantidad, precio, categoria) VALUES(:idcar, :nombre,:cant, :prec, :cat)",
                    idcar = id_carrito,
                    nombre = nombre,
                    cant = cantidad,
                    prec = precio,
                    cat = categoria)
    return jsonify(res)

@app.route("/cambiarCantidad")
def cambiarCantidad():
    id_carrito = cargarCarrito()
    idDetalleCarrito = request.args.get("idDetalleCarrito")
    cantidad = request.args.get("cantidad")
    res = db.execute("UPDATE detalle_carrito SET cantidad = :cantidad WHERE id_detalle_carrito = :iddc", cantidad = cantidad, iddc = idDetalleCarrito)
    return jsonify(res)

@app.route("/comprar")
def comprar():
    id_carrito = cargarCarrito()
    res = db.execute("UPDATE carrito SET estado= 1 WHERE id_carrito = :ic", ic = id_carrito)
    return jsonify(res)
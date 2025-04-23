#Victor Aguayo & Liam Martinez
#Projecte de sintesi IndieNest
#Document d'execució del servidor


#Llibreries necesaries per la execucio de la web
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

#Son diferent recursos que dicten el funcionament de la pagina
app = Flask(__name__)
#Esto creo que es la contraseña del mysql CREO
app.secret_key = "hello"
#Te diria que es donde pone lo de sqlite no se que
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/dbindienest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(seconds=10)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))


    def __init__(self, name, email):
        self.name = name
        self.email = email


#Mostra la base de la pagina web
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())
#Muestra la tienda
@app.route("/shop")
def shop():
    return render_template("shop.html")

#Funcionament de la pagina login (una vegada que has fet el login es quedara iniciat el temps que dicti el parametre: app.permanent_session_lifetime)
@app.route("/login", methods=["POST", "GET"])
def login():
    
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        pswrd = request.form["pw"]
        session["user"] = user
        session["pswrd"] = pswrd

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
          usr = users(user, "")
          db.session.add(usr)
          db.session.commit()
        
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
       
        return render_template("login.html")

@app.route("/conditions")
def conditions():
        return render_template("conditions.html")

#Detecte si tens usuari i si no et torna al apartat login
@app.route("/profile", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        pswrd = session["pswrd"]
        if request.method == "POST":
            email = request.form ["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
        else:
            if "email" in session:
                email = session["email"]
                
        return render_template("user.html", email=email, user=user, pswrd = pswrd)
    else:
        return redirect(url_for("login"))
    

#Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    session.pop("pswrd", None)

    return redirect(url_for("login"))

#Fa que s'executi el servei flask
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True )
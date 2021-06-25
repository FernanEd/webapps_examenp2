import uuid
from flask.helpers import flash
from app import app
from flask import render_template, url_for, redirect, request
from app.forms import LoginForm, NotaForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_manager, LoginManager, login_required
from app.models import Nota, UUID, User
from app import db
import pytz
from datetime import datetime, timezone

# ----[DATE]----

@app.template_filter('formatdate')
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=pytz.timezone('America/Monterrey'))

# ----[LOGIN]----

login_manager = LoginManager(app)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login?next=' + request.path)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form=LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email = email).first()
        if user is None or not user.check_password(form.password.data):
            flash("Correo o contraseña no validos")
            return redirect(url_for("login"))
        else:
            login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    else:
        return render_template("login.html", form=form)
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form=RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email = email).first()
        if user is None and form.password.data==form.password_confirm.data:
            user = User(email=email)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for("index"))
        else:
            flash("El usuario ya existe o tu contraseñas no coincide")
            return redirect(url_for("register"))
    else:
        return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ----[RUTAS]----

@app.route("/")
@login_required
def index():
    notas = Nota.query.filter_by(user_id=current_user.id).all()
    return render_template("index.html", notas=notas)

@app.route("/crearnota", methods=['GET', 'POST'])
@login_required
def crearnota():
    form=NotaForm()  
    if form.validate_on_submit():
        nuevanota = Nota(desc=form.desc.data, user_id=current_user.id)
        db.session.add(nuevanota)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template("crear_nota.html", form=form)

@app.route("/borrarnota/<int:id>", methods=['GET', 'POST'])
@login_required
def borrarnota(id):
    nota = Nota.query.get(id)
    if request.method == 'POST':
        db.session.delete(nota)
        db.session.commit()
        print(id)
        return redirect(url_for('index'))

    return render_template("borrar_nota.html", nota=nota)

@app.route("/compartirnota/<int:id>", methods=['GET', 'POST'])
@login_required
def compartirnota(id):
    random_uuid = uuid.uuid4().__str__()
    nuevo_uuid = UUID(uuid=random_uuid, nota_id=id, user_id=current_user.id)
    db.session.add(nuevo_uuid)
    db.session.commit()
    return render_template("compartir_nota.html", link=(request.url_root).removesuffix('/') + url_for('nota', id=random_uuid))

@app.route("/nota/<id>", methods=['GET', 'POST'])
def nota(id):
    uuid = UUID.query.get(id)
    nota = Nota.query.get(uuid.nota_id)
    author = User.query.get(uuid.user_id)
    return render_template("ver_nota.html", nota=nota, author=author)

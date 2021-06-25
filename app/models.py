from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

class User(UserMixin, db.Model):
  id                =db.Column(db.Integer, primary_key=True)
  email             =db.Column(db.String(120), index=True, unique=True)
  password_hash     =db.Column(db.String(128)) 

  def set_password(self, password):
    self.password_hash =generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  # Relaciones
  notas             =db.relationship("Nota", backref="user", lazy="dynamic")
  uuids             =db.relationship("UUID", backref="user", lazy="dynamic")

class Nota(db.Model):
  id                =db.Column(db.Integer,primary_key=True)
  desc              =db.Column(db.String(255))
  timestamp         =db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id           =db.Column(db.Integer, db.ForeignKey("user.id"))

class UUID(db.Model):
  uuid              =db.Column(db.String(255), primary_key=True)
  nota_id           =db.Column(db.Integer)
  user_id           =db.Column(db.Integer, db.ForeignKey("user.id"))
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms import validators
from wtforms.validators import DataRequired, Email, Length

# Forms para las paginas
# Login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Por favor llene el campo')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Por favor llene el campo')])
    remember_me = BooleanField('Recuerdame')
    submit = SubmitField('Entrar')

# Registro
class RegisterForm (FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Por favor llene el campo'), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Por favor llene el campo')])
    password_confirm = PasswordField('Confirmar contraseña', validators=[DataRequired(message='Por favor llene el campo')])
    submit = SubmitField('Registrarse')

class NotaForm (FlaskForm):
    desc = TextAreaField('Descripción', validators=[DataRequired(message='Por favor llene el campo'), Length(max=255, message='El mensaje debe ser menor de 255')])
    submit = SubmitField('Crear nota')
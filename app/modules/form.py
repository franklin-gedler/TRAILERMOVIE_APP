from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email

class Contactanos(FlaskForm):
    clientname = StringField('Tu Nombre', validators=[InputRequired()])
    email = StringField('Tu Email (Te llegará una copia de la solicitud)', validators=[InputRequired(), Email()])
    comment = TextAreaField('Solicita tus trailers...', validators=[InputRequired()])
    submit = SubmitField('Enviar')


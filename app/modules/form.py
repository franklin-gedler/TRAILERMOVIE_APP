from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired, ValidationError

class Contactanos(FlaskForm):
    clientname = StringField('Tu Nombre', validators=[InputRequired()])
    email = StringField('Tu Email (Te llegará una copia de la solicitud)', validators=[InputRequired(), Email()])
    comment = TextAreaField('Solicita tus trailers...', validators=[InputRequired()])
    submit = SubmitField('Enviar')

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class CreateFormPeliculaSerie(FlaskForm):
    name_type = SelectField('Tipo de Nombre', choices=[('name_pelicula', 'Nombre Película'), ('name_serie', 'Nombre Serie')], validators=[DataRequired()])
    name_type_input = StringField('Nombre', validators=[DataRequired()])
    video_id = StringField('Video ID', validators=[DataRequired()])
    link_img = StringField('Link de la imagen', validators=[DataRequired()])
    details = TextAreaField('Detalles', validators=[DataRequired()])

class GetformPeliculaSerie(FlaskForm):
    name_pelicula_serie = StringField('Nombre', validators=[DataRequired()])

class UpdateFormPeliculaSerie(FlaskForm):
    name_pelicula_serie = StringField('Nombre', validators=[DataRequired()])
    new_name = StringField('New Name')
    details = TextAreaField('Details')
    link_img = StringField('Link Image')
    new_name = StringField('New Name')
    video_id = StringField('Video ID')
    
class DeleteformPeliculaSerie(FlaskForm):
    name_type = SelectField('Tipo de Nombre', choices=[('pelicula', 'Nombre Pelicula'), ('serie', 'Nombre Serie')], validators=[DataRequired()])
    name_type_input = StringField('Nombre', validators=[DataRequired()])

class CreateFormUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    #allow = StringField('Allow', validators=[DataRequired()])
    allow = SelectField('Allow', choices=[('read', 'Read'), ('write', 'Write')], validators=[DataRequired()])

class GetformUser(FlaskForm):
    username = StringField('username', validators=[DataRequired()])

class UpdateFormUser(FlaskForm):
    user = StringField('Username', validators=[DataRequired()])
    username = StringField('New Name')
    password = PasswordField("Password")
    allow = SelectField('Allow', choices=[('read', 'Read'), ('write', 'Write')])

class DeleteformUser(FlaskForm):
    user = StringField('Username', validators=[DataRequired()])


class FormContainer(FlaskForm):
    def __init__(self):
        #self.contactanos = Contactanos()
        #self.login_form = LoginForm()
        super(FormContainer, self).__init__()
        self.create_form_pelicula_serie = CreateFormPeliculaSerie()
        self.get_form_pelicula_serie = GetformPeliculaSerie()
        self.update_form_pelicula_serie = UpdateFormPeliculaSerie()
        self.delete_form_pelicula_serie = DeleteformPeliculaSerie()
        self.create_form_user = CreateFormUser()
        self.get_form_user = GetformUser()
        self.update_form_user = UpdateFormUser()
        self.delete_form_user = DeleteformUser()

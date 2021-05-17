from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email(), DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


class SignUpForm(FlaskForm):
    name = StringField("Name", render_kw={"placeholder": "Name"})
    email = StringField("Email", validators=[Email(), DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign up")


class AlbumForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", render_kw={"placeholder": "Description..."})
    date = DateField("Creation date", format='%Y-%m-%d', render_kw={'type': 'date'})


class CreateAlbumForm(AlbumForm):
    submit = SubmitField("Create")


class EditAlbumForm(AlbumForm):
    submit = SubmitField("Edit")

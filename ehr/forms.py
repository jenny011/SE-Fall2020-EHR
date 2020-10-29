from flask.app import Flask
from flask_wtf import FlaskForm
from werkzeug import datastructures
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, ValidationError

class LoginForm(FlaskForm):

    role = RadioField(label="Role",
                      choices=[('doctor', "I am a doctor"), ('nurse', 'I am a nurse'), ('patient', 'I am a patient')],
                      validators=[DataRequired()])
    id = StringField(label="ID",
                     validators=[DataRequired()])
    password = PasswordField(label="Password",
                             validators=[DataRequired()])
    submit = SubmitField(label="Sign in")

class RegisterForm(FlaskForm):
    role = RadioField(label="Role",
                      choices=[('doctor', "I am a doctor"), ('nurse', 'I am a nurse'), ('patient', 'I am a patient')],
                      validators=[DataRequired()])
    id = StringField(label="ID",
                     validators=[DataRequired()])
    password = PasswordField(label="Password",
                             validators=[DataRequired()])
    first_name = StringField(label="FisrtName", validators=[DataRequired()])
    last_name = StringField(label="LastName", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired(),Email()])
    phone = StringField(label="Phone")
    submit = SubmitField(label="Register")

    # any function with function name "validation_<field name>"
    # will run automatically together with the above validator.
    def validate_id_email(self, id, email):
        check_id = User.query.filter_by(id=id)
        if check_id is not None:
            raise ValidationError("ID is taken, please use a different one or contact us.")
        check_email = User.query.filter_by(email=email)
        if check_email is not None:
            raise ValidationError("Email is taken, please use a different one or contact us.")

from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField, SubmitField,  BooleanField, TextAreaField
from flask_wtf.file import FileAllowed,FileField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from Ecommerce_pkg.models import User
from flask_login import current_user 

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min = 5,max = 20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8)])
    confirm_password = PasswordField('Confirm password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up!')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("The username is already taken")

    def validate_email(self, email):
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError("There already exixts an account with this email")

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min = 5,max = 20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Update info')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError("The username is already taken")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError("There already exixts an account with this email")

class addproductsForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    price = StringField('price',validators=[DataRequired()])
    description =TextAreaField('description',validators=[DataRequired()])
    category = SelectField('Category',choices=[("Outdoor sports","Outdoor sports"),("Water sports","Water sports"),("Fitness","Fitness"),("Nutrition and Supplements","Nutrition and Supplements")])
    image = FileField('Image',validators=[FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField('Submit')